from __future__ import annotations 

from dataclasses import dataclass
from phasescreen.base import Coordinate, PolarScreen, Flip, noflip , cart2pol, reorient 
import numpy as np

@dataclass
class DiskScreenMaker:
    """ A screen maker for a pupil represented by a disk with obsional central obscuration 

    Args:
        diameter: Pupil disk diameter in user unit 
        center: (x,y) coordinate of the pupil disk in diameter unit.
            these are coordinate from the center of the screen 
        obscuaration_diameter: Central obscuration diameter 
        phase_angle: define the angle of the projected phase on the screen 
        phass_flip: A valid flip for the phase projection ("". "x", "xy", "y")
    
    
    Exemple: 
        
        from phasescreen import DiskScreenMaker, zernpol, zernpol_func  
        from matplotlib.pylab import plt
        import numpy as np

        screen = DiskScreenMaker( diameter = 1.0, obscuration_diameter=0.2, center=(0.3,0) ).make_screen( (800,800), 400.0)
        
        phases = zernpol_func( zernpol(["tip","tilt","defocus"]), screen.r, screen.theta, masked=False) 
        amps = np.array( [0.2, 1.0, 0.5] )
        phases = ( phases.T*  amps ).T 
        plt.imshow( screen.construct(phases.sum(axis=0) ) )
        plt.show()        

        
            
    """
    diameter: float = 1.0
    center: Coordinate = Coordinate(0.0, 0.0) 
    obscuration_diameter: float = 0.0 
    phase_angle: float = 0.0 
    phase_flip: Flip = noflip 
    
    def make_screen(self, shape, scale: float = 1.0)->PolarScreen:
        ny, nx = shape 
        
        x0, y0 = self.center 
        px0, py0 = (  nx/2.0+x0*scale , ny/2.0+y0*scale)
        
        p_radius = self.diameter*scale / 2.0
        
        X, Y = np.meshgrid( (np.arange(nx)-px0)/p_radius , (np.arange(ny)-py0)/p_radius )
        r, theta = cart2pol(X, Y)
        obscuration = self.obscuration_diameter/ self.diameter
        mask = (r <= 1.0) *( r>=obscuration)
        theta = reorient(theta, self.phase_flip, self.phase_angle)
        return PolarScreen( mask, r[mask], theta[mask], p_radius, Coordinate(px0, py0) )



if __name__=="__main__":
    from matplotlib.pylab import plt 
    import zernpol 
    screen = DiskScreenMaker( center=(.3, 0), diameter=2, phase_angle=np.pi/8.0, obscuration_diameter=0.2  ).make_screen( [800,800], 300.0 )
    
    modes =  zernpol.zernpol_func( zernpol.zernpol(["tip", "tilt"]), screen.r, screen.theta, masked=False )
    phase =  np.sum( modes * np.array( [2.0, 0.0])[:,None], axis=0)
    plt.imshow(screen.construct(phase)) 

    plt.show()
