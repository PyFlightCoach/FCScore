
import streamlit as st
import tempfile
import os
from flightanalysis import State, Box
from flightdata import Flight
from io import StringIO
from src.pages import Stage
from pathlib import Path


ss = st.session_state


def write():

    if not st.checkbox("parse state directly", False): 
        bin_file = st.file_uploader("Upload a BIN File", ["BIN", "bin"])
        box_file = st.file_uploader("Upload a box file", ["F3A", "f3a"])    

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
            ss.default_start_offset = 1000
            ss.default_end_offset = -1000
            ss.stage += 1
            st.experimental_rerun()

    else:
        csv_file = st.file_uploader("Upload a State csv File", ["csv"])

        if csv_file and st.button("Read State File"):
            with tempfile.TemporaryDirectory() as td:
                f_name = os.path.join(td, 'test.bin')
                with open(f_name, 'wb') as fh:
                    fh.write(csv_file.getvalue())

                ss.flown = State.from_csv(f_name)
        
            ss.default_start_offset = 0
            ss.default_end_offset = 0

            ss.stage += 1
            st.experimental_rerun()


if __name__ == '__main__':
    if not "stage" in ss:
        ss.stage = Stage.START

    if ss.stage == Stage.START:
        
        with st.expander("Description"):
            st.markdown(Path(__file__.replace(".py", ".md")).read_text())
        write()
    else:
        
        st.write(f"parsed log length {len(ss.flown.data)}")
        st.write(ss.stage)