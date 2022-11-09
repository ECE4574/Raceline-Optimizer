from scipy.optimize import Bounds, minimize, minimize_scalar
from scipy.interpolate import splev, splprep
import numpy as np
import math 
from raceline import RaceLine
from helpers import VelocityMap


class Optimizer:
    """The Optimizer class handles Optimizing a raceline around
    a track for a specific car and a specific track
    """
    def __init__(self,track, vehicle) -> None:
        self.track = track
        self.vehicle = vehicle 
        self.update(np.full(track.size, 0.5))
        self.vel = VelocityMap(vehicle)
        self.epshis = {}
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
    def lap_time(self):
        """Calcualtes lap time by taking the change in distance from one
        point to the other divided by the velocity at that point. 
        The sum of the time it takes to get from one point to another 
        ois the lap time 

        Returns:
            float: laptime 
        """
        return np.sum(np.diff(self.raceline.s) / self.vel.v_final)
    def update_vel(self):
        samples = self.raceline.s[:-1]
        curv = self.raceline.curvature(samples)
        self.vel.reset(samples, self.raceline.length, curv)
        
    def fun(self,alphas):
        """Updates the path and the velocitymap after very iteration of the minimzing
        alogirthm and returns the lap time

        Args:
            alphas (list): alpha values from 0 to 1

        Returns:
            float: lap time
        """
        self.update(alphas)
        self.update_vel()
        return self.lap_time()
    def minEps(self):
        def fun(eps):
            self.minCurve(eps)
            self.update_vel()
            lap_time = self.lap_time()
            self.epshis[lap_time] =  eps
            return lap_time
        res = minimize_scalar(
            fun=fun,
            method='bounded',
            bounds=(0, 1)
            )
        
        return res.x
    
    def minCurve(self, eps):
        def fun(alphas):
            """Updates the path after very iteration of the minimzing
            alogirthm and returns the new sum of curvature of the track 
            Args:
                alphas (list): alpha values from 0 to 1
            Returns:
                float: squared sum of the curvature along track
            """
            self.update(alphas)
            return self.raceline.gamma2()*eps + (1-eps)* self.raceline.length
        res = minimize(
            fun=fun,
            x0 = np.full(self.track.size, 0.5),
            method='L-BFGS-B',
            bounds=Bounds(0.0, 1.0)
            
        )
        self.update(res.x)
        
        
    def minLapTime(self):
        best_eps = self.minEps()
        self.minCurve(best_eps)
        self.update_vel()
        
        
