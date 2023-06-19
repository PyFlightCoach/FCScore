
from dash import Dash, html, dcc, Output, Input, State, dash_table, dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Scheme, Format
import dash_bootstrap_components as dbc
import plotly.express as px
from json import load
from io import StringIO
import base64
from flightanalysis import *
from typing import List

from flightdata import Flight
import numpy as np 
import pandas as pd
import plotly.graph_objects as go
from multiprocessing import Process, Queue
from datetime import datetime
from time import time, sleep
from uuid import uuid4
from threading import Thread
from geometry import Quaternion

app_data = {}

def cleanup():
    ad = {k: data["last_hb"] for k, data in app_data.items()}
    last_allowed_hb = time() - 10
    pop_list = [k for k, v in ad.items() if last_allowed_hb > v]
    
    for pop_sess in pop_list:
        print(f"removing user {pop_sess}")
        app_data.pop(pop_sess)


app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server
def serve_layout():
    session_id = str(uuid4())

    app_data[session_id] = dict(
        started = time(),
        status = ["initializing"],
        last_hb = time(),
        analysis = ScheduleAnalysis(),
        q = Queue(),
        p = None,
    )
    app_data[session_id]["status"].append([f"user connected at {datetime.now()}, session_id = {session_id}, active users = {len(app_data)}"],)
    return html.Div(
    [
        dcc.Store(data=session_id, id='session-id'),
        dbc.Row([dbc.Col(dcc.Upload(
                id='upload-json',
                children=html.Div(['Drag and Drop or ',html.A('Select FC json file')]),
                style={
                    'width': '100%',
                    'height': '30px',
                    'lineHeight': '30px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '2px',
                    'textAlign': 'center',
                    'margin': '10px'
                })),
                dbc.Col(html.Div(id="status"), align="center")
        ],justify="center"),
        dbc.Row(
            [

                dbc.Col(
                    [
                        html.P("Once a json file is loaded scores should start to appear in the table below"),
                        html.P("You can click on a row of the table to see a plot of the flown manoeuvre and the corrected template"),
                        DataTable(
                            id='score-table', 
                            fill_width=False, 
                            columns=[
                                dict(id="name", name="name"),
                                dict(id="k", name="k", type="numeric"),
                                dict(id="inter_dg", name="inter_dg", type="numeric", format=Format(precision=2, scheme=Scheme.decimal)),
                                dict(id="intra_dg", name="intra_dg", type="numeric", format=Format(precision=2, scheme=Scheme.decimal)),
                                dict(id="exit_dg", name="exit_dg", type="numeric", format=Format(precision=2, scheme=Scheme.decimal)),
                                dict(id="score", name="score", type="numeric", format=Format(precision=2, scheme=Scheme.decimal)),
                            ]
                        ), 
                        html.H2(id="total-score")
                    ], width=3),
                dbc.Col(dcc.Graph(id='plot-analysis', style={'height': '90vh'}))
            ]
        ),
        dcc.Interval(
			id='interval-component',
			interval=3000, # in milliseconds
			n_intervals=0
		),
        html.P(id='placeholder') 
    ]    
)

app.layout = serve_layout


def parsefcj(data: dict, q: Queue):
    try:
        q.put("parsing flight data")
        flight = Flight.from_fc_json(data)

        q.put("parsing flightline")
        box = Box.from_fcjson_parmameters(data["parameters"])

        q.put("generating state information")
        state = State.from_flight(flight, box).splitter_labels(data["mans"])

        q.put(f"reading {data['parameters']['schedule'][1]} schedule definition")
        sdef = get_schedule_definition(data["parameters"]["schedule"][1])
        
        for mid in range(17):
            q.put(f"Analysing manoeuvre {mid+1}")
            q.put(ManoeuvreAnalysis.build(sdef[mid], state.get_meid(mid+1)).to_dict())

        q.put(f"Analysis Complete")
    except Exception as ex:
        q.put(f"Analysis Error: {ex.message}")
    

@app.callback(
    Output('placeholder', 'children'), 
    Input('upload-json', 'contents'),
    Input('session-id', 'data')
)
def update_output(contents, session_id):
    ad = app_data[session_id]
    if not ad["p"] is None:
        ad["status"].append("Cannot Restart")
    elif contents is not None:
        ad["status"].append("started")
        content_type, content_string = contents.split(',')
        data = load(StringIO(base64.b64decode(content_string).decode('utf-8')))
        ad["p"] = Process(target=parsefcj, args=(data, ad["q"]))
        ad["p"].start()
    return None


@app.callback(
    Output('status', 'children'),
    Output('score-table', 'data'),
    Output('total-score', 'children'),
    Input('interval-component', 'n_intervals'),
    Input('session-id', 'data')
)
def update_status(i, session_id):
    ad = app_data[session_id]
    ad["last_hb"] = time()
    if not ad["q"].empty():
        message = ad["q"].get()
        if isinstance(message, str):
            ad["status"].append(message)
            if message == "Analysis Complete":
                pass
        elif isinstance(message, dict):
            ma = ManoeuvreAnalysis.from_dict(message)
            
            ma.intra_dgs = ma.mdef.mps.collect(ma.intended)
            ma.intra_dg = sum([dg.value for dg in ma.intra_dgs])

            ma.inter_dgs = ma.intended.analyse(ma.aligned, ma.intended_template)
            ma.inter_dg = ma.inter_dgs.downgrade()

            ad["analysis"].add(ma)
            ad["status"].append(f"Completed Analysis of {ma.mdef.info.name}")
    cleanup()

    scores = []

    for ma in ad["analysis"]:
        scores.append(dict(
            name=ma.mdef.info.short_name,
            k=ma.mdef.info.k,
            inter_dg = ma.inter_dg,
            intra_dg = ma.intra_dg,
        ))

    if len(scores) > 0:
        scores = pd.DataFrame(scores)
        scores["score"] = np.maximum(0, 10 - scores.inter_dg - scores.intra_dg)
    else:
        scores = pd.DataFrame(columns = ["name","k", "inter_dg", "intra_dg", "exit_dg", "score"])
    return ad["status"][-1], scores.to_dict('records'), sum(scores.score * scores.k)

@app.callback(
    Output('plot-analysis', 'figure'), 
    Input('score-table', 'active_cell'),
    Input('session-id', 'data')
)
def update_graphs(active_cell, session_id):
    if active_cell:
        return app_data[session_id]["analysis"][active_cell["row"]].plot_3d(nmodels=30)
    else:
        return go.Figure()




if __name__ == "__main__":

    app.run_server(host="0.0.0.0", port=8050, debug=True)