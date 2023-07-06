
from dash import Dash, html, dcc, Output, Input, State, dash_table, dcc
from dash.dash_table import DataTable
from dash.dash_table.Format import Scheme, Format
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
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


app_data = {}


app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.config["suppress_callback_exceptions"] = True
server = app.server


def serve_layout():
    session_id = str(uuid4())

    app_data[session_id] = dict(
        started = time(),
        status = ["initialized"],
        last_hb = time(),
        manoeuvre_count = 17,
        analysis = ScheduleAnalysis(),
        q = Queue(),
        p = None,
        scores = pd.DataFrame(columns = ["name","k", "inter_dg", "intra_dg", "exit_dg", "score"]),
        total_score = 0.0,
    )
    app_data[session_id]["status"].append([f"user connected at {datetime.now()}, session_id = {session_id}, active users = {len(app_data)}"],)
    return html.Div(
    [
        dcc.Store(data=session_id, id='session-id'),
        dcc.Interval(id="session-heartbeat", interval=5000, n_intervals=0),
        dbc.Row([
            html.Div(id="uploader", children=dcc.Upload(
                    id='upload-json',
                    children=html.Div(['Drag and Drop or ',html.A('Select FC json file')]),
                    style=dict(width='100%',height='30px',lineHeight='30px',borderWidth='1px',borderStyle='dashed',borderRadius='2px',textAlign='center',margin='10px')
            )),
            html.Div(id="status"),
            dcc.Interval(id='upload-status-interval',interval=3000, n_intervals=0, disabled=True)
        ]),
        dbc.Row([
            dbc.Col([html.Div(id="score-table"), html.H2(id="total-score")], width=3),
            dbc.Col([html.Div(id="summary-man")])
        ]),
        dbc.Row([html.Div(id="summary-el")])
    ]
)

app.layout = serve_layout


@app.callback(
    Output('uploader', 'children'),
    Output('upload-status-interval', 'disabled', allow_duplicate=True),
    Input('upload-json', 'contents'),
    Input('session-id', 'data'),
    prevent_initial_call=True
)
def upload_fcjson(contents, session_id):
    ad = app_data[session_id]
    if contents is not None:

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
                q.put(f"manoeuvre count = {len(sdef)}")
                for mid in range(17):
                    q.put(f"Analysing manoeuvre {mid+1}")
                    q.put(ManoeuvreAnalysis.build(sdef[mid], state.get_meid(mid+1)).to_dict())

                q.put(f"Analysis Complete")
            except Exception as ex:
                q.put(f"Analysis Error: {ex.message}")

        content_type, content_string = contents.split(',')
        data = load(StringIO(base64.b64decode(content_string).decode('utf-8')))
        ad["p"] = Process(target=parsefcj, args=(data, ad["q"]))
        ad["p"].start()
        ad["status"].append(f"Analysing {data['name']}")
        return None, False
    else:
        raise PreventUpdate()


@app.callback(
    Output('session-heartbeat', 'disabled'),
    Input('session-heartbeat', 'n_intervals'),
    Input('session-id', 'data')
)
def user_manager(i, session_id):
    ad = app_data[session_id]
    ad["last_hb"] = time()
    
    sessions = {k: data["last_hb"] for k, data in app_data.items()}
    last_allowed_hb = time() - 7
    pop_list = [k for k, v in sessions.items() if last_allowed_hb > v]
    
    for pop_sess in pop_list:
        print(f"removing user {pop_sess}")
        app_data.pop(pop_sess)

    return False


@app.callback(
    Output('status', 'children'),
    Output('upload-status-interval', 'disabled', allow_duplicate=True),
    Input('upload-status-interval', 'n_intervals'),
    Input('session-id', 'data'),
    prevent_initial_call=True
)
def update_status(i, session_id):
    ad = app_data[session_id]
    if not ad["q"].empty():
        message = ad["q"].get()
        if isinstance(message, str):
            ad["status"].append(message)
            if message == "Analysis Complete":
                pass
            elif "manoeuvre count =" in message:
                ad["manoeuvre_count"] = int(message.split("=")[1])
        elif isinstance(message, dict):
            ma = ManoeuvreAnalysis.from_dict(message)
            ad["analysis"].add(ma)
            ad["status"].append(f"Completed Analysis of {ma.mdef.info.name}")
    
    return ad["status"][-1], ad["status"][-1] == "Analysis Complete"


@app.callback(
    Output('score-table', 'children'),
    Output('total-score', 'children'),
    Input('upload-status-interval', 'n_intervals'),
    Input('session-id', 'data') 
)
def update_scores(i, session_id):
    ad = app_data[session_id]
    if len(ad["analysis"]) > len(ad["scores"]):
        scores = []
        for ma in ad["analysis"]:
            if not hasattr(ma, "intra_dg"):
                ma.intra_dgs = ma.intended.analyse(ma.aligned, ma.intended_template)
                ma.intra_dg = ma.intra_dgs.downgrade()
            if not hasattr(ma, "inter_dg"):
                ma.inter_dgs = ma.mdef.mps.collect(ma.intended)
                ma.inter_dg = sum([dg.value for dg in ma.inter_dgs])

            scores.append(dict(
                name=ma.mdef.info.short_name,
                k=ma.mdef.info.k,
                inter_dg = ma.inter_dg,
                intra_dg = ma.intra_dg,
                score = max(0, 10 - ma.inter_dg - ma.intra_dg)
            ))
        
        ad["scores"] = pd.DataFrame(scores)
        ad["total_score"] = f"{sum(ad['scores'].score * ad['scores'].k):.2f}"
        df = ad["scores"].round(2)

        dt =  DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="scoretab")

        return dt, ad["total_score"]
    else:
        if len(ad["scores"]) == ad["manoeuvre_count"]:
            ad["status"].append("Analysis Complete")
        raise PreventUpdate()


@app.callback(
    Output('summary-man', 'children'), 
    Input('scoretab', 'active_cell'),
    Input('session-id', 'data'),
    prevent_initial_call=True
)
def update_graphs(active_cell, session_id):
    if active_cell:
        ma = app_data[session_id]["analysis"][active_cell["row"]]

        graph = dcc.Graph(id='plot-analysis', style={'height': '90vh'}, figure=ma.plot_3d(nmodels=30))
    
        inter_df = ma.inter_dgs.downgrade_df().round(2)
        inter_tab = DataTable( inter_df.to_dict('records'), [{"name": i, "id": i} for i in inter_df.columns])

        intra_df = ma.intra_dgs.downgrade_df().round(2).reset_index()
        intra_tab = DataTable( intra_df.to_dict('records'), [{"name": i, "id": i} for i in intra_df.columns])

        return [graph, inter_tab, intra_tab]
    raise PreventUpdate()


if __name__ == "__main__":

    app.run_server(host="0.0.0.0", port=8050, debug=True)