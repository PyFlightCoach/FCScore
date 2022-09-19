import streamlit as st
ss = st.session_state
from flightanalysis import State
from geometry import Transformation
from src.pages import Stage


def write():

    st.write("Performing preliminary alignment")

    dist, aligned = State.align(ss.flown, ss.template, 10)

    st.write(f"alignment complete, dist={dist}")

    st.write("measuring elements")

    ss.intended = ss.p23.match_intention(ss.template[0].transform, aligned)

    st.write("creating intended template 1")
    tf = Transformation(
        aligned[0].pos,
        aligned[0].att.closest_principal()
    )
    ss.template = ss.intended.create_template(tf)

    st.write("performing secondary aligment")

    dist, ss.aligned = State.align(ss.flown, ss.template, 10, False)

    st.write(f"alignment complete, dist={dist}")

    st.write("measuring elements")

    ss.intended = ss.p23.match_intention(tf, ss.aligned)

    st.write("creating intended template 2")

    ss.template = ss.intended.create_template(Transformation(
        ss.aligned[0].pos,
        ss.aligned[0].att.closest_principal()
    ))

    st.write("updating schedule definition defaults")

    ss.definition.update_defaults(ss.intended)

    st.write("creating corrected template")

    ss.corrected, ss.corrected_template = ss.definition.create_template(ss.flown.pos.y.mean(), ss.wind)

    ss.stage +=1

    st.experimental_rerun()


if __name__ == '__main__':
    from pathlib import Path

    from src.pages.select_schedule import populate
    from flightanalysis import State
    from flightplotting import plotdtw
    if not "stage" in ss:
        ss.stage = Stage.SPLITFLIGHT
        ss.flown = State.from_csv("test_data/flown_scored_state.csv")
        populate("P23")

    if ss.stage == Stage.SPLITFLIGHT:
        with st.expander("Description"):
            st.markdown(Path(__file__.replace(".py", ".md")).read_text())
        write()
    else:
        
        if ss.stage == Stage.CHECKSPLIT:
            st.plotly_chart(plotdtw(ss.aligned, ss.p23.to_list()))
            st.write(f"moving to next stage: {ss.stage}")

            ss.aligned.to_csv("test_data/aligned.csv")
            ss.template.to_csv("test_data/intended_template.csv")
            ss.corrected_template.to_csv("test_data/corrected_template.csv")
            