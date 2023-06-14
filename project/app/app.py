
from dash import Dash, html, dcc, Output, Input, State, dash_table, dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Scheme, Format
import dash_bootstrap_components as dbc
import plotly.express as px
from json import load
from io import StringIO
import base64
from flightanalysis import State, Box
from flightanalysis.data import get_schedule_definition
from flightanalysis.schedule import *
from flightanalysis.fc_score import ManoeuvreAnalysis, ScheduleAnalysis
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


app_data = {}

app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server
def serve_layout():
    session_id = str(uuid4())

    app_data[session_id] = dict(
        started = time(),
        status = [f"user connected at {datetime.now()}, session_id = {session_id}"],
        last_hb = time(),
        analysis = ScheduleAnalysis(),
        q = Queue(),
        p = None,
    )
    return html.Div(
    [
        dcc.Store(data=session_id, id='session-id'),
        dbc.Row([dbc.Col(dcc.Upload(
                id='upload-json',
                children=html.Div(['Drag and Drop or ',html.A('Select File')]),
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
                        DataTable(
                            id='score-table', 
                            fill_width=False, 
                            columns=[
                                dict(id="name", name="name"),
                                dict(id="k", name="k", type="numeric"),
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
            ad["analysis"].add(ma)
            ad["status"].append(f"Completed Analysis of {ma.mdef.info.name}")
    return ad["status"][-1], ad["analysis"].summary_df().to_dict('records'), ad["analysis"].total_score()


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


def cleanup():
    while True:
        sleep(5)
        ad = {k: data["last_hb"] for k, data in app_data.items()}
        last_allowed_hb = time() - 10
        pop_list = [k for k, v in ad.items() if last_allowed_hb > v]
#        for session_id, data in app_data.items():
#            if time() > data["last_hb"] + 5:
#                pop_list.append(session_id)
            
        for pop_sess in pop_list:
            app_data.pop(pop_sess)

if __name__ == "__main__":
    th = Thread(target=cleanup, daemon=True).start()

    app.run_server(host="0.0.0.0", port=8050, debug=True)