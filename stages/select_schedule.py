import streamlit as st
ss = st.session_state
from stages import Stage, t_from_i
import numpy as np
from flightanalysis.data.p23 import create_p23
from geometry import Transformation
from flightplotting import plotsec


def write():
    _sch = st.selectbox("select schedule", ["P23"])

    ss.wind=np.sign(ss.flown[0].vel.x[0])

    ss.definition = dict(
        P23 = create_p23
    )[_sch](ss.wind)

    ss.p23, ss.template = ss.definition.create_template(ss.flown.pos.y.mean(), ss.wind)

    st.plotly_chart(plotsec(ss.template, scale=3))

    if st.button("confirm sequence selection"):
        ss.stage += 1


if __name__ == '__main__':
    from flightanalysis import State
    if not "stage" in ss:
        ss.stage = Stage.SELECTSCHEDULE
        ss.flown = State.from_csv("test_data/flown_scored_state.csv")

    if ss.stage == Stage.SELECTSCHEDULE:
        write()
    else:
        
        if ss.stage == Stage.SPLITFLIGHT:
            st.write(f"moving to next stage: {ss.stage}")

            