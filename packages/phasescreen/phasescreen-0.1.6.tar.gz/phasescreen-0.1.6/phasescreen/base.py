from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from typing import Callable, NamedTuple
import numpy as np 

class Coordinate(NamedTuple):
    x: float 
    y: float 

class Size(NamedTuple):
    width: float 
    height: float 

class Flip(NamedTuple):
    x: int 
    y: int 

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(r, theta):
    return (r*np.cos(theta), 
            r*np.sin(theta)
        )

_flip_func_loockup = {
(1,  1) : lambda t: t, 
(-1, 1) : lambda t: -t + np.pi,
(-1,-1) : lambda t: t  + np.pi,
(1, -1) : lambda t: -t,
}   

_flip_func_loockup[None] = _flip_func_loockup[(1,1)]
_flip_func_loockup[''] = _flip_func_loockup[(1,1)]
_flip_func_loockup['x'] = _flip_func_loockup[(-1,1)]
_flip_func_loockup['xy'] = _flip_func_loockup[(-1,-1)]
_flip_func_loockup['yx'] = _flip_func_loockup[(-1,-1)]
_flip_func_loockup['y'] = _flip_func_loockup[(1,-1)]
noflip = (1,1)


def reorient(theta, flip, offset_angle):
    try:
        f = _flip_func_loockup[flip]
    except KeyError:
        raise ValueError(f"flip argument not understood got: {flip!r}")
    if offset_angle: # avoid to add 0.0 to a big theta array 
        return f(theta) + offset_angle
    else:
        return f(theta)


class _BaseScreen:
    def construct(self, phases:np.ndarray , dtype=None, fill: np.ScalarType = np.nan, ma: bool = False):
        phases = np.asarray( phases) 
        if dtype is None:
            dtype = phases.dtype
        screen = np.ndarray( phases.shape[:-1]+self.mask.shape, dtype=dtype)
        screen[...] = fill
        screen[..., self.mask] = phases 
        if ma:
            return np.ma.masked_array( screen , ~self.mask)
        return screen
    
    def deconstruct(self, images:np.ndarray)->np.ndarray:
        return np.asarray(images)[..., self.mask]


@dataclass
class PolarScreen(_BaseScreen):
    mask: np.ndarray
    r: np.ndarray
    theta: np.ndarray 
    scale: float 
    origin: Coordinate
    def to_polar(self)->PolarScreen:
        return PolarScreen( self.mask, self.r, self.theta, self.scale, self.origin )
    
    def to_cartezian(self)->CartezianScreen:
        x, y = pol2cart(self.r, self.theta)
        return CartezianScreen( self.mask, x, y, (self.scale, self.scale), self.origin)


@dataclass
class CartezianScreen(_BaseScreen):
    mask: np.ndarray
    x: np.ndarray
    y: np.ndarray 
    scale: tuple[float, float]  
    origin: Coordinate
    def to_polar(self)->PolarScreen:
        r, theta = cart2pol( self.x, self.y)
        return PolarScreen( self.mask, r, theta, np.mean(self.scale), self.origin )
    
    def to_cartezian(self)->CartezianScreen:
        return CartezianScreen( self.mask, self.x, self.y, self.scale, self.origin)

    
def make_polar_screen( mask: np.ndarray, phase_angle: float = 0.0, phase_flip: str | None = None )->PolarScreen:
    """ Make a polar screen from a pupill mask 

    Guess the center with the barycenter of the mask 
    The radius is the maximum distance between center and illuminated pixels. 
    
    Args:
        mask: image array of boolean. True are illuminated pixels  
        phase_angle: Offset angle of the projected phase
        phase_flip: Flip "", "x" or "xy" flip of the phase 
            
    Returns:
        screen (PolarScreen): normalized screen built from mask 

    """
    ny, nx = mask.shape 

    xc, yc = mask_barycenter(mask)
    x, y = np.meshgrid( np.arange(nx) - xc,  np.arange(ny)-yc )
    r, theta = cart2pol( x, y)
    r = r[mask]
    theta = theta[mask]
    theta = reorient(theta, phase_flip, phase_angle ) 
    scale = np.max( r ) 
    r /= scale 
    return PolarScreen( mask, r, theta, scale, Coordinate(xc, yc) )

def mask_barycenter(mask)->Coordinate:
    ny, nx = mask.shape 
    x, y = np.meshgrid( np.arange(nx), np.arange(ny))
    xc = np.mean( x[mask] )
    yc = np.mean( y[mask] )
    return Coordinate(xc, yc)




    

     


