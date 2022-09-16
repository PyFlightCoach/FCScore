from stages import Stage, t_from_i
import streamlit as st
ss = st.session_state

import numpy as np
from flightplotting import plotsec
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events



def write():

    match ss.stage:
        case Stage.STARTSEQUENCE:
            label = "flight_start"
            default=1000
        case Stage.ENDSEQUENCE:
            label = "flight_end"
            default = len(ss.flown.data) - 1000

    if not label in ss:
        ss[label] = default

    selected_point = ss.flown[t_from_i(ss[label])].pos

    start_id, end_id = st.select_slider(
        "plot range", 
        np.linspace(0, len(ss.flown.data) -1, dtype="int"),   
        (0, len(ss.flown.data)-1)
    )

    fig = plotsec(ss.flown[t_from_i(start_id):t_from_i(end_id)], scale=2)        
    fig.add_trace(go.Scatter3d(
        x=selected_point.x, 
        y=selected_point.y, 
        z=selected_point.z, 
        name=label, 
        showlegend=False
    ))

    selected_point = plotly_events(fig)

    if len(selected_point) == 1:
        ss[label] = selected_point[0]["pointNumber"] + start_id
        st.experimental_rerun()

    if st.button(f"confirm {label}"):
        #ss.flown = ss.flown[
        #    t_from_i(ss.flight_start):t_from_i(ss.flight_end)
        #]

        if ss.stage == Stage.ENDSEQUENCE: 
            ss.flown = ss.flown[t_from_i(ss.flight_start):t_from_i(ss.flight_end)]

        ss.stage += 1
        
        st.experimental_rerun()


if __name__ == '__main__':
    from flightanalysis import State
    if not "stage" in ss:
        ss.stage = Stage.STARTSEQUENCE
        ss.flown = State.from_csv("test_data/flown_state.csv")

    if ss.stage == Stage.STARTSEQUENCE or ss.stage == Stage.ENDSEQUENCE:
        write()
    else:
        
        if ss.stage == Stage.SELECTSCHEDULE: 
            st.write(f"start sequence time {t_from_i(ss.flight_start)}")
            st.write(f"end sequence time {t_from_i(ss.flight_end)}")
            st.write(f"moving to next stage: {ss.stage}")

            