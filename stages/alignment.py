import streamlit as st
ss = st.session_state
from flightanalysis import State
from geometry import Transformation


def write():

    st.write("Performing preliminary alignment")

    dist, aligned = State.align(ss.flown, ss.template, 10)

    st.write(f"alignment complete, dist={dist}")

    st.write("measuring elements")

    ss.p23 = ss.p23.match_intention(ss.template[0].transform, aligned)

    st.write("creating intended template 1")

    ss.template = ss.p23.create_template(Transformation(
        aligned[0].pos,
        aligned[0].att.closest_principal()
    ))

    st.write("performing secondary aligment")

    dist, ss.aligned = State.align(ss.flown, ss.template, 10, False)

    st.write(f"alignment complete, dist={dist}")

    st.write("measuring elements")

    ss.p23 = ss.p23.match_intention(ss.template[0].transform, aligned)

    st.write("creating intended template 2")

    ss.template = ss.p23.create_template(Transformation(
        ss.aligned[0].pos,
        ss.aligned[0].att.closest_principal()
    ))

    st.write("updating schedule definition defaults")

    ss.p23_def.update_defaults(ss.intended)

    st.write("creating corrected template")

    ss.corrected, ss.corrected_template = ss.p23_def.create_template(ss.flown.pos.y.mean(), ss.wind)

    ss.stage +=1

    st.experimental_rerun()