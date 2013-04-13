from bootstrapping_olympics.library.nuisances.popcode.popcode_functions import popcode
from procgraph import simple_block
import numpy as np

@simple_block
def scan2image(readings, max_reading=6, resolution=240):
    readings = readings / max_reading
    readings = np.clip(readings, 0, 1) 
    return popcode(readings, resolution)
