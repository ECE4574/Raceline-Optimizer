from math import sqrt
import numpy as np

class Track:
    def __init__(self,left,right):
        self.left = left
        self.right = right
        self.size = self.left[0].size - 1 # -1 since the track is closed the first and last points are the same
        self.diff = self.right - self.left
    def alphas_to_point(self,alphas):
      alphas = np.append(alphas, alphas[0])
      i = np.nonzero(alphas != -1)[0]
      return self.left[:,i] + (alphas[i] * self.diff[:,i])
    def points_to_alphas(self, points):
      return (points-self.left)/self.diff
  
class Vehical:
    def __init__(self,mass = 200, friction = 1.5, engineForce = 3114):
        self.mass = mass
        self.friCof = friction
        self.engineForce = engineForce
        
class VelocityMap:
    def __init__(self, vehicle):
        self.vehicle = vehicle
       
    def reset(self,samples,sample_max, curv):
        self.samples = samples
        self.sample_max = sample_max
        self.curv = curv
        self.limit_vel()
        self.limit_acc(self.curv)
        self.limit_decel(self.curv)
        self.v_final = np.minimum(self.v_acclim, self.v_declim)
        
    def traction(self, v, curv ):
        friction_force = self.vehicle.friCof * self.vehicle.mass * 9.81
        centriptal_froce = self.vehicle.mass * v**2 * curv
        if friction_force <= centriptal_froce:
            return 0
        else:
            return sqrt(friction_force**2-centriptal_froce**2)
    def engine_force(self, v):
        return self.vehicle.engineForce
    
    def limit_vel(self):
        self.v = np.sqrt(self.vehicle.friCof*(9.81/self.curv)) #max velocity to match centriptal force
    def limit_acc(self,curv_in):
        start = np.argmin(self.v)
        v = np.array(self.v)
        k = curv_in
        s = self.samples
        for i in range(start, self.samples.size+start):
            prev = (i-1)%self.samples.size
            curr = i%self.samples.size
            if self.sample_max is None: continue
            if v[curr] > v[prev]:
                traction = self.traction(v[prev], k[prev])
                force = min(self.engine_force(v[prev]), traction)
                accel = force / self.vehicle.mass
                ds =  s[curr] - s[prev] if curr != 0 else self.sample_max - curr
                vlim = sqrt(v[prev]**2 + 2*accel*ds)
                v[curr] = min(v[curr], vlim)

       
        self.v_acclim = v
        
    
    def limit_decel(self, curv_in):

       
        start = np.argmin(self.v)
        v = np.array(self.v)
        k = curv_in
        s = self.samples

       
        for i in range(start, start - self.samples.size , -1):
            next = (i+1)%self.samples.size
            curr = i%self.samples.size
            if self.sample_max is None: continue
            if v[curr] > v[next]:
                traction = self.traction(v[next], k[next])
                decel = traction / self.vehicle.mass
             
                #change in distance
                ds =  s[next] - s[curr] if next != 0 else self.sample_max - s[curr]
                vlim = sqrt(v[next]**2 + 2*decel*ds)
                v[curr] = min(v[curr], vlim)

        
        self.v_declim = v
   