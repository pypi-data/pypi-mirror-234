from __future__ import annotations
from phasescreen._elt_pupil_utils import generateEeltPupilMask
from dataclasses import dataclass
from phasescreen.base import Coordinate, Flip,  PolarScreen, cart2pol, noflip, reorient 

import numpy as np 
# generateEeltPupilMask( 500, 1.0, 250, 250, 40/400, 0.00, 0)


@dataclass
class EltScreenMaker:
    diameter: float = 40.0
    angle: float =0.0
    center: Coordinate = Coordinate(0, 0)
    spider_width: float = 1.0
    gap: float = 0.0
    phase_angle: float = 0.0 
    phase_flip: Flip = noflip 

    def make_screen(self, shape, scale:float|None = None )->PolarScreen:
        ny, nx = shape 
        size =  int(max( ny, nx ) )
        
        if scale is None:
            scale = size / self.diameter 
        x0, y0 = self.center 
        p_x, p_y = x0*scale+size/2.0, y0*scale+size/2.0  
         
        p_radius = self.diameter * scale / 2.0
        
        elt_scale = 40.0/self.diameter
    
        # inverse p_y and p_x (not the same convention ) 
        mask = generateEeltPupilMask( size, self.spider_width*elt_scale , p_y, p_x, elt_scale/scale, self.gap*elt_scale, self.angle*180/np.pi )

        if nx==ny:
            pass
        elif ny>nx:
            dx = (nx-size)//2 
            dy = 0
            mask = mask[:,dx:dx+nx] 
        else:
            dx = 0
            dy = (nx-ny)//2
            mask = mask[dy:dy+ny,:] 


        vx = (np.arange(nx)-p_x-dx )/ p_radius   
        vy = (np.arange(ny)-p_y-dy )/ p_radius

        x, y = np.meshgrid(vx, vy) 
        r, theta = cart2pol( x, y) 
        theta = reorient(theta,  self.phase_flip, self.phase_angle) 
        return PolarScreen( mask, r[mask], theta[mask], p_radius, Coordinate(p_x, p_y) )


if __name__ == "__main__":
    from phasescreen.utils import  PhaseImageMaker
    screen = EltScreenMaker( center=( 0.5, 0.0), angle=np.pi/8.0, phase_angle = np.pi/4 ).make_screen( (500,800), 400/40 )
    import zernpol 
    modes =  zernpol.zernpol_func(  zernpol.zernpol(range(1, 5)), screen.r, screen.theta, masked=False )
    # phase = (modes.T *  [0, 0.0, 1.0, 0.0]).sum(axis=1)
    phase =  (modes * np.array( [0, 0.0, 1.0, 0.0] )[:,None] ).sum(axis=0)
    
    # pm = PhaseImageMaker( screen, zernpol.zernpol_func, zernpol.zernpol(range(1, 10))  )
    
    from matplotlib.pylab import plt 
    plt.imshow(screen.construct(phase))
    plt.show()
    print( screen.scale)


        



        
        
