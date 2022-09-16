
import streamlit as st
import tempfile
import os
from flightanalysis import State, Box
from flightdata import Flight
from io import StringIO
from stages import Stage



ss = st.session_state

def write():

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
        ss.stage += 1
        st.experimental_rerun()


if __name__ == '__main__':
    if not "stage" in ss:
        ss.stage = Stage.START

    if ss.stage == Stage.START:
        write()
    else:
        st.write(f"parsed log length {len(ss.flown.data)}")
        st.write(ss.stage)