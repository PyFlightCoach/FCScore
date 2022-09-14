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
        _sopt = st.selectbox("select option", ["start", "end"], 0)

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
        from flightanalysis.data.p23 import create_p23
        from geometry import Transformation

        if not "aligned" in ss:
            _sch = st.selectbox("select schedule", ["P23"])
            

            wind=np.sign(ss.flown[0].vel.x[0])
            ss.p23_def = dict(
                P23 = create_p23
            )[_sch](wind)
            
            if st.button("run alignment (takes a while)"):

                st.write(f"creating template schedule at {ss.flown.pos.y.mean()}m")
                
                p23, template = ss.p23_def.create_template(ss.flown.pos.y.mean(), wind)

                st.write("Performing preliminary alignment")

                dist, aligned = State.align(ss.flown, template, 10)

                st.write(f"alignment complete, dist={dist}")

                st.write("measuring elements")

                intended = p23.match_intention(template[0].transform, aligned)

                st.write("creating intended template 1")

                intended_template = intended.create_template(Transformation(
                    aligned[0].pos,
                    aligned[0].att.closest_principal()
                ))
                
                st.write("performing secondary aligment")

                dist, ss.aligned = State.align(ss.flown, intended_template, 10, False)

                st.write(f"alignment complete, dist={dist}")

                st.write("measuring elements")

                ss.intended = p23.match_intention(template[0].transform, aligned)

                st.write("creating intended template 2")

                ss.intended_template = ss.intended.create_template(Transformation(
                    ss.aligned[0].pos,
                    ss.aligned[0].att.closest_principal()
                ))

                st.write("updating schedule definition defaults")

                ss.p23_def.update_defaults(ss.intended)

                st.write("creating corrected template")

                ss.corrected, ss.corrected_template = ss.p23_def.create_template(ss.flown.pos.y.mean(), wind)

                st.experimental_rerun()
        else:
            from flightplotting import plotdtw
            manid = st.slider("select manoeuvre", 1, 17, 1)
            man = ss.intended[manid-1]
            st.write(man.uid)
            fig=plotdtw(man.get_data(ss.aligned), man.all_elements.to_list())
            st.plotly_chart(fig)

            if st.button("Score"):
                ss.stage="scoring"
                st.experimental_rerun()

    if ss.stage == "scoring":
        manid = st.slider("select manoeuvre", 1, 17, 1)
        #man=st.selectbox("select manoeuvre", [m.info.short_name for m in ss.p23_def])

        man = ss.intended[manid-1]
        elid = st.slider("select element", 1, len(man.elements.data), 1)
        el=man.elements[elid-1]

        aligned = man.get_data(ss.aligned)
        intended = man.get_data(ss.intended_template)
        corrected = man.get_data(ss.corrected_template)
        
        transform = man.get_data(ss.aligned)[0].transform
        results =  ss.p23_def[man.uid].mps.collect(man)

        intra_results = man.analyse(
            man.get_data(ss.aligned),
            man.get_data(ss.intended_template)
        )
        interdg=results.downgrade()
        intradg = intra_results.downgrade()

        score = 10 - interdg - intradg

        st.write(f"downgrades: - {intra_results.downgrade_list()} (intra) - {interdg} (inter)")
        st.title(f"{man.uid}: {score}")

        st.plotly_chart(plotsec(aligned, nmodels=10, scale=5))

        st.write("Inter Element Downgrades:")
        st.dataframe(results.downgrade_df())

        st.write(f"Intra Element Results for element {el.uid}, {el.describe()}")

        st.dataframe(intra_results[el.uid].results.downgrade_df())


    if st.button("remove log"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()