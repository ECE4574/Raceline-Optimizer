import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json

from optimizer import Optimizer
import raceline
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

f = open('buckmore.json') 
data = json.load(f)
left = np.array([data["left"]["x"], data["left"]["y"]]) #left coor
right = np.array([data["right"]["x"], data["right"]["y"]]) #right corr

track = Track(left,right)
opt = Optimizer(track)
opt.min_curve()
LCLR = 'tab:gray'
RCLR = 'tab:gray'

def drawTrack(left, right):
  plt.figure() 
  plt.plot(left[0], left[1], color=LCLR, linestyle='solid', zorder=1, linewidth=1)
  plt.plot(right[0], right[1], color=LCLR, linestyle='solid', zorder=1, linewidth=1)
  plt.plot(opt.raceline.path[0], opt.raceline.path[1], color="red", linestyle='solid', zorder=1, linewidth=1)
  plt.show()

drawTrack(left,right)