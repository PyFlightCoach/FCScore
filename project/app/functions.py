from json import load
from io import StringIO
import base64
from flightanalysis import State, Box
from flightanalysis.data import get_schedule_definition
from flightanalysis.schedule import *
from flightanalysis.fc_score import ManoeuvreAnalysis, ScheduleAnalysis
from typing import List
from flightdata import Flight
import numpy as np 
import pandas as pd
import plotly.graph_objects as go
from multiprocessing import Process, Array, Value, Queue









def parsefcj(data: dict, q: Queue):
    

    flight = Flight.from_fc_json(data)
    box = Box.from_fcjson_parmameters(data["parameters"])
    state = State.from_flight(flight, box).splitter_labels(data["mans"])
    sdef = get_schedule_definition(data["parameters"]["schedule"][1])
    for mid in range(17):
        q.put(ManoeuvreAnalysis.build(sdef[mid], state.get_meid(mid+1)))
