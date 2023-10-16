from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np 
from phasescreen.base import PolarScreen, CartezianScreen 

def rms_norm(phase:np.ndarray):
    values /= np.std(phase)

def pv_norm(phase:np.ndarray):
    values /=  (np.max(values)-np.min(phase))

def no_norm(_):
    pass

def phase(
        func,  
        screen: PolarScreen|CartezianScreen, 
        coef: tuple|list[tuple], 
        amplitude: list[float] | None = None,  
        norm: Callable = no_norm
    ):
    coordinates = _get_coordinates(screen)
    if _is_scalar(coef):
        phase =  _scalar_phase( func, coordinates, amplitude) 
    else:
        phase = _vect_phase( func, coordinates, amplitude) 
    norm( phase) 
    return phase     

def _is_scalar( coef ):
    return isinstance( coef, tuple)

def _get_coordinates(screen: PolarScreen | CartezianScreen ):
    if isinstance(screen, PolarScreen):
        coordinates = (screen.r, screen.theta)
    elif isinstance(screen, CartezianScreen):
        coordinates = ( screen.x, screen.y ) 
    else:
        raise ValueError(f"Expecting a PolarScreen or CartezianScreen as second argument got a {type(screen)}")
    return coordinates

def _scalar_phase( 
        func: Callable, 
        coef: tuple|list[tuple], 
        coordinates: tuple[np.ndarray, np.ndarray], 
        amplitude: list[float] | None = None,  
    ):
    amplitude = 1.0 if amplitude is None else amplitude 
    return  func( coef, *coordinates)* amplitude

def _vect_phase(
       func: Callable, 
       coordinates: tuple[np.ndarray, np.ndarray], 
       coef: list[tuple], 
       amplitude: list[float] | None = None
    ):
    x1, _ = coordinates 
    values = np.zeros( x1.shape, float)
    if amplitudes is None:
        amplitudes = [1.0]*len(coef)
    for c,a in zip( coef, amplitude):
        values +=  func( c, *coordinates) * a
    return values 



def phase_image(
        func,  
        screen: PolarScreen|CartezianScreen , 
        coef: tuple|list[tuple], 
        amplitude: list[float] | None = None,
        fill=np.nan, 
        dtype=float, 
        ma: bool = False, 
        norm: Callable = no_norm
    ):
    values = phase( func, screen, coef, amplitude, norm=norm)
    return screen.construct( values, dtype=dtype, fill=fill, ma=ma)


    
@dataclass 
class PhaseImageMaker:
    """ This object make phase screen images

    Args:
        screen: A ScreenPolar or ScreenCartezian as returned by e.g. :func:`DiskScreenMaker.make_screen` 
        func: A function of signature  ``f( coef, r, theta)``  (or ``f(coef, x, y) if screen is in cartezian coordinates)
            This is the function describing the polynomial base system.  By default it is the zernike function.
        polynoms: A list of polynoms representig the polynomial base system decomposition.
            By default this is 40 Zernike polynoms sorted by the Noll system

    Exemple:
    
        from phasescreen.phasescreen import DiskScreenMaker, PhaseImageMaker, zernpol, zernpol_func  
        from matplotlib.pylab import plt
        import numpy as np

        screen = DiskScreenMaker( diameter = 1.0, obscuration_diameter=0.2, center=(0.3,0) ).make_screen( (800,800), 400.0)
        phase_maker = PhaseImageMaker( screen, func=zernpol_func, polynoms = zernpol(["tip","tilt","defocus"]) )
        plt.imshow( phase_maker.make_phase( [ 1.0, 0.2, 0.5] ) )
        plt.show()


    """
    screen: PolarScreen| CartezianScreen
    func: Callable 
    polynoms: tuple|list[tuple] 

    def make_phase(self, amplitudes:list|dict ):
        if isinstance(amplitudes,dict):
            iterator = amplitudes.items()
        else:
            iterator = zip(self.polynoms, amplitudes)
        coordinates = _get_coordinates( self.screen )
        x1, _ = coordinates 
        phase = np.zeros( x1.shape, float )
        for pol,a  in iterator:
            phase += _scalar_phase( self.func, pol,  coordinates, a )
        return self.screen.construct(phase) 

