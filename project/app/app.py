
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
from flightanalysis.fc_score import ManoeuvreAnalysis
from typing import List
from flightdata import Flight
import numpy as np 
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server



app.layout = html.Div(
    [
        dbc.Row([html.Div([dcc.Upload(
                id='upload-json',
                children=html.Div(['Drag and Drop or ',html.A('Select File')]),
                style={'width': '100%','height': '60px'})
        ])]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(DataTable(
                            id='score-table', 
                            fill_width=False, 
                            columns=[
                                dict(id="name", name="name"),
                                dict(id="k", name="k", type="numeric"),
                                dict(id="score", name="score", type="numeric", format=Format(precision=2, scheme=Scheme.decimal)),
                            ]
                        )), 
                        dbc.Row(html.H2(id="total-score"))
                    ], width=3, align="center"),
                dbc.Col(dcc.Graph(id='plot-analysis', style={'height': '90vh'}))
            ]
        )
    ]    
)

analyses: List[ManoeuvreAnalysis] = []


def parsefcj(content):
    content_type, content_string = content.split(',')
    data = load(StringIO(base64.b64decode(content_string).decode('utf-8')))

    flight = Flight.from_fc_json(data)
    box = Box.from_fcjson_parmameters(data["parameters"])
    state = State.from_flight(flight, box).splitter_labels(data["mans"])
    sdef = get_schedule_definition(data["parameters"]["schedule"][1])
    analyses.clear()
    for mid in range(2):
        analyses.append(ManoeuvreAnalysis.build(sdef[mid], state.get_meid(mid+1)))
    
    df = pd.DataFrame([[an.mdef.info.short_name, an.mdef.info.k, an.score] for an in analyses], columns=["name", "k", "score"])
    #if "scores" in data:
    #    df["manual_scores"] = data["scores"][1:-1]
    
    return df

@app.callback(
    Output('total-score', 'children'),
    Output('score-table', 'data'), 
    Input('upload-json', 'contents')
)
def update_output(list_of_contents):
    if list_of_contents is not None:
        df = parsefcj(list_of_contents)
        return f"total = {sum(df.score * df.k)}", df.to_dict('records')
    else:
        return None, None


@app.callback(Output('plot-analysis', 'figure'), Input('score-table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell:
        return analyses[active_cell["row"]].plot_3d()
    else:
        return go.Figure()
    

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)