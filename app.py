import numpy as np
import pandas as pd

import streamlit as st
from streamlit_plotly_events import plotly_events
from flightdata import Flight
from flightanalysis import State, Box
import tempfile
import os
from io import StringIO
import plotly.graph_objects as go
from flightplotting import plotsec


ss = st.session_state

def check_flight():
    if "flown" in ss:
        return ss.flown is not None
    else:
        return False

if not check_flight():
    bin_file = st.file_uploader("Upload a BIN File", ["BIN", "bin"])
    box_file = st.file_uploader("Upload a box file", ["f3a"])    
    if bin_file and box_file and st.button("Create State Object"):
        with tempfile.TemporaryDirectory() as td:
            f_name = os.path.join(td, 'test.bin')
            with open(f_name, 'wb') as fh:
                fh.write(bin_file.getvalue())
            ss["flown"] = State.from_flight(
                Flight.from_log(f_name).flying_only(), 
                Box.from_f3a_zone(StringIO(box_file.getvalue().decode("utf-8")))
            )
            bin_file = None
            box_file = None
        st.experimental_rerun()

if check_flight():

    if not "stage" in ss:
        ss["stage"] = "select scored flight"

    if ss.stage == "select scored flight":      

        if not "flight_start" in ss:
            ss["flight_start"] = 1000

        if not "flight_end" in ss:
            ss["flight_end"] = len(ss.flown.data) - 2000

        t_from_i = lambda index : ss.flown.data.index[index]

        _fsps = dict(
            start = ss.flown[t_from_i(ss.flight_start)].pos,
            end = ss.flown[t_from_i(ss.flight_end)].pos
        )

        start_id, end_id = st.select_slider(
            "plot range", 
            np.linspace(0, len(ss.flown.data) -1, dtype="int"),   
            (0, len(ss.flown.data)-1)
        )

        fig = plotsec(ss.flown[t_from_i(start_id):t_from_i(end_id)], scale=2)        
        fig.add_trace(go.Scatter3d(x=_fsps["start"].x, y=_fsps["start"].y, z=_fsps["start"].z, name="start", showlegend=False))
        fig.add_trace(go.Scatter3d(x=_fsps["end"].x, y=_fsps["end"].y, z=_fsps["end"].z, name="end", showlegend=False))

        selected_point = plotly_events(fig)
        _sopt = st.selectbox("select option", ["start", "end"])

        if len(selected_point) == 1:
            ss[f"flight_{_sopt}"] = selected_point[0]["pointNumber"] + start_id
            st.experimental_rerun()

        if st.button("split_log"):
            ss.flown = ss.flown[
                t_from_i(ss.flight_start):t_from_i(ss.flight_end)
            ]
            ss.stage = "split flight"
            st.experimental_rerun()


    if ss.stage == "split flight":
        st.plotly_chart(plotsec(ss.flown))



    if st.button("remove log"):
        del ss["flown"]
        del ss.stage
        st.experimental_rerun()