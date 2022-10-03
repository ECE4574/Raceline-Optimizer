from scipy.optimize import Bounds, minimize, minimize_scalar
from scipy.interpolate import splev, splprep
import numpy as np
import math 
from raceline import RaceLine


class Optimizer:
    """The Optimizer class handles Optimizing a raceline around
    a track for a specific car and a specific track
    """
    def __init__(self,track) -> None:
        self.track = track
        self.update(np.full(track.size, 0.5))
    def update(self,alphas):
        """Update function updates the path for a certain 
        inputted alpahs 

        Args:
            alphas (list): alphas are perctanges from 0-1 outlining
            how far th epath is from the left side of the track. 0 being
            on the left edge of the track and 1 being on the right edge of
            the track. 
        """
        self.alphas = alphas
        path = self.track.alphas_to_point(alphas) 
        self.raceline = RaceLine(path)
        self.raceline.sample_every_meter() 
       
        
    def fun(self,alphas):
        """Updates the path after very iteration of the minimzing
        alogirthm and returns the new sum of curvature of the track 

        Args:
            alphas (list): alpha values from 0 to 1

        Returns:
            float: squared sum of the curvature along track
        """
        self.update(alphas)
        return self.raceline.gamma2(self.raceline.s)
    

    def min_curve(self):
        """minimzes the curvrature of the raceline using the 'L-BFGS-B' 
        algorithm
        """
        res = minimize(
            fun=self.fun,
            x0=np.full(self.track.size, 0.5),
            method='L-BFGS-B',
            bounds=Bounds(0.0, 1.0)
            )
        self.update(res.x)
    
