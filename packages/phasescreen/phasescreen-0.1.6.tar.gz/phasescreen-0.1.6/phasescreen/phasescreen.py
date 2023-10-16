

from functools import wraps
from phasescreen.base import (
    PolarScreen, 
    CartezianScreen,
    make_polar_screen, 
)
from phasescreen.utils import rms_norm, pv_norm, no_norm
from phasescreen.disk_pupil import DiskScreenMaker 
from phasescreen.rectangular_pupil import RectangleScreenMaker 
from phasescreen.elt_pupil import EltScreenMaker

