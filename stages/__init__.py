
from enum import Enum
import streamlit as st

t_from_i = lambda index : st.session_state.flown.data.index[index]


class Stage(Enum):
    START=0
    STARTSEQUENCE=1
    ENDSEQUENCE=2
    SELECTSCHEDULE=3
    SPLITFLIGHT=4
    CHECKSPLIT = 5
    SCORES = 6

    def __add__(self, value):
        return Stage(self.value + value)



from . import create_state
from . import select_point
from . import select_schedule
from . import alignment
from . import check_alignment
from . import scores
