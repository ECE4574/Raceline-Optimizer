
import numpy as np
import matplotlib.pyplot as plt
import json
from helpers import Vehical, Track
import matplotlib.animation as animation
from optimizer import Optimizer
from trackgenerator import TrackDataGenerator
from matplotlib.collections import LineCollection


    
LCLR = 'tab:gray'
RCLR = 'tab:gray' 
def update_line(num, data,data1,data2 ,line,line2,line3):
    line.set_data(data[..., :num])
    line2.set_data(data1[..., :num])
    line3.set_data(data2[..., :num])
    return line,
def drawTrackAnimation(left, raceline, right):
  fig = plt.figure() 
  plt.xlim(-100, 1500)
  plt.ylim(-100, 1000)
  l, = plt.plot([], [], 'r-')
  l2, = plt.plot([], [], 'b-')
  l3, = plt.plot([], [], 'g-')
  data = np.vstack((left[0],left[1]))
  data1 = np.vstack((right[0],right[1]))
  data2 = np.vstack((raceline[0], raceline[1]))
  line_ani = animation.FuncAnimation(fig, update_line, frames=4000,
                            fargs=(data, data1,data2, l,l2, l3), interval=10, blit=False)
  plt.show()
  
def drawTrack(left,right):

  fig = plt.figure()
  plt.plot(left[0], left[1], color=LCLR, linestyle='solid', zorder=1, linewidth=1)
  plt.plot(right[0], right[1], color=LCLR, linestyle='solid', zorder=1, linewidth=1)
  # plt.plot(opt.raceline.path[0],opt.raceline.path[1], color="green", linestyle='solid', zorder=1, linewidth=1)
  # plt.plot(opt.raceline.path[0],opt.raceline.path[1], marker="o", markersize=2, markeredgecolor="red", markerfacecolor="green")
  # plt.plot(opt.raceline.position(opt.raceline.s)[0],opt.raceline.position(opt.raceline.s)[1], color="red", linestyle='solid', zorder=1, linewidth=1)

  plt.show()
  


def plot_trajectory(left, right, samples, velocities):
  """
  Plot path with velocity colour map.
  """
  # Set up velocity gradient segments
  plt.figure() 
  plt.plot(left[0], left[1], color=LCLR, linestyle='solid', linewidth=1, zorder=1)
  plt.plot(right[0], right[1], color=LCLR, linestyle='solid', linewidth=1, zorder=1)
  p = samples.T.reshape(-1, 1, 2)
  segments = np.concatenate([p[:-1], p[1:]], axis=1)
  norm = plt.Normalize(np.amin(velocities), np.amax(velocities))
  lc = LineCollection(
    segments, array=velocities, norm=norm, linewidth=2, zorder=2
  )
  plt.gca().add_collection(lc)
  plt.gcf().colorbar(
    lc, orientation="horizontal", label="Velocity (m/s)", pad=0.05, aspect=30
  )
  plt.gca().set_aspect('equal', adjustable='box')
  plt.axis('off')
  plt.show()
  
  
  
f = open('buckmore.json') 
data = json.load(f)
left = np.array([data["left"]["x"], data["left"]["y"]]) #left coor
right = np.array([data["right"]["x"], data["right"]["y"]]) #right corr

# tg = TrackDataGenerator()
# coord = tg.get_center_line_coord_from_raw_image('raw_track_image/track.png')
# width = 50
# tg.save_track_data_to_file('track.json', coord, width)
# left, center,right, _ = tg.read_track_lines_v2('track.json', sample_num=300, smooth_kernel_length=4)
# off = 4
# left = np.array([left[0][::4],left[1][::4]])
# right = np.array([right[0][::4], right[1][::4]])

drawTrack(left,right)
track = Track(left,right)
ve = Vehical(200,1.5,3114)
opt = Optimizer(track, ve)
opt.minLapTime()

    


  
plot_trajectory(left,right,opt.raceline.position(opt.raceline.s), opt.vel.v_final)