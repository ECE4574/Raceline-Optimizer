"""
raceline.cpp    Walid Zeineldin     Virginia Tech       Dec 5th, 2020 
This file holdes the data strcture that holds information on a raceline 
"""
from scipy.interpolate import splev, splprep
import math
import numpy as np

class RaceLine:
    def __init__(self, path):
        self.path = path
        cum_dist = np.cumsum(np.linalg.norm(np.diff(path, axis=1), axis=0))
        self.dists = np.append(0,cum_dist)
        self.spline, _ = splprep(path, u=self.dists, k=3, s=0, per=1)
        self.length = self.dists[-1]
        self.sample_every_meter()
    def gamma2(self):
        """Calcualtes the square sum of curvature of the path around the track


        Returns:
            float: square of sum of curvature 
        """
        
        ddx, ddy = splev(self.s, self.spline, 2)
        return np.sum(ddx**2 + ddy**2)
    def curvature(self, samples = None):
        if samples is None:
            samples = self.dists
        ddx, ddy = splev(samples, self.spline, 2)
        return np.sqrt(ddx**2 + ddy**2)
    def sample_every_meter(self):
        # Sample every metre
        #split track into sectors from 0 to length generating length samples  
        self.s = np.linspace(0, self.length, math.ceil(self.length))
    def position(self, s=None):
        """Returns x-y coordinates of sample points."""
        x, y = splev(s, self.spline)
        return np.array([x, y])