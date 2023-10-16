from __future__ import annotations
from dataclasses import dataclass 
from phasescreen.base import Coordinate, Size, Flip, noflip , PolarScreen, reorient,cart2pol
import numpy as np 

@dataclass
class RectangleScreenMaker:
    center: Coordinate = Coordinate(0.0, 0.0)
    size: Size|None = None 
    angle: float = 0.0 
    flip: Flip = noflip
    inscribed: float =  True
    
    def make_screen(self, shape, scale: float = 1.0)->PolarScreen:
        ny, nx = shape 
        x0, y0 = self.center 
        px0, py0 = (  nx/2.0+x0*scale , ny/2.0+y0*scale)
        if self.size is None:
            p_height, p_width = shape 
        else:
            width, height = self.size 
            p_width,p_height = width*scale, height*scale 
        X, Y = np.meshgrid( (np.arange(nx)-px0)/p_width , (np.arange(ny)-py0)/p_height )

        r, theta = cart2pol(X, Y)
        mask = (np.abs( X)<=0.5 ) * (np.abs( Y )<=0.5)
        theta = reorient(theta, self.flip, self.angle)
        return PolarScreen( mask, r[mask], theta[mask], max(p_width, p_height), Coordinate(px0, py0) )





