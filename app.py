import numpy as np
import pandas as pd

import streamlit as st
ss = st.session_state

from stages import *

def check_flight():
    if "flown" in ss:
        return ss.flown is not None
    else:
        return False

if not "stage" in ss or not check_flight():
    ss.stage = Stage.START


pages = {
    Stage.START: create_state,
    Stage.STARTSEQUENCE: select_point,
    Stage.ENDSEQUENCE: select_point,
    Stage.SELECTSCHEDULE: select_schedule,
    Stage.SPLITFLIGHT: alignment,
    Stage.CHECKSPLIT: check_alignment,
    Stage.SCORES: scores
}

pages[ss.stage].write()