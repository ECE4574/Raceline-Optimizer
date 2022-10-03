from scipy.interpolate import splev, splprep
import math
import numpy as np

class RaceLine:
    def __init__(self, path):
        self.path = path
        self.dists = self.cumulative_distances(path)
        self.spline, _ = splprep(path, u=self.dists, k=3, s=0, per=1)
        self.length = self.dists[-1]
        self.sample_every_meter()
    def cumulative_distances(self,points):
        """Calculate the cumulative distance along the track 

        Args:
            points (list): list of points of the path around the track

        Returns:
            _type_: array of cumsum at every point
        """
        d = np.cumsum(np.linalg.norm(np.diff(points, axis=1), axis=0))
        return np.append(0, d)
    def gamma2(self):
        """calcualtes the square sum of curvature of the path around the track


        Returns:
            float: square of sum of curvature 
        """
        
        ddx, ddy = splev(self.s, self.spline, 2)
        return np.sum(ddx**2 + ddy**2)
    def curvature(self):
        ddx, ddy = splev(self.dists, self.spline, 2)
        return np.sum(ddx**2 + ddy**2)
    def sample_every_meter(self):
        # Sample every metre
        #split track into sectors from 0 to length generating length samples  
        self.s = np.linspace(0, self.length, math.ceil(self.length))