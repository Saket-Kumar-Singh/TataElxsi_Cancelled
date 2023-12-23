from .utils import find_conv, st_dev
from .resources import np, noise, gaussian_filter 
import reeds_sheep as rs
from pydantic import BaseModel, EmailStr

class map: 
  def __init__(self, dem, obstacle):
    self.dem = dem
    self.obstacle = obstacle
    self.dem_temp = find_conv(dem, conv = 20)
    self.dem_st_dev = st_dev(dem, self.dem_temp)
    self.add_obstacles()
    self.dim = np.shape(np.array(self.obstacle)) 
    self.bfs()   
    
  def add_obstacles(self):  
    for i in range(len(self.dem)):
      for j in range(len(self.dem[0])):
        if self.dem_st_dev[i][j] > 8 :
          self.obstacle[i][j] = 1
  
  def bfs(self):
    lst = []
    for i in range(self.dim[0]):
      for j in range(self.dim[1]):
        if (self.obstacle[i][j] == 1): 
          lst.append((i,j))
    dir = [-1,0,1]
    # dir = [-1,0,1]
    while len(lst):
      p = lst.pop(0)
      for i in range(3):
        for j in range(3):
          try: 
            if (p[0] + dir[i] < self.dim[0]) and (p[1]+dir[j] < self.dim[1]) and (p[0] + dir[i] > 0) and (p[1] + dir[j] > 0) and ((self.obstacle[p[0]+dir[i]][p[1]+dir[j]] == 0) or (self.obstacle[p[0]+dir[i]][p[1]+dir[j]] > self.obstacle[p[0]][p[1]] + 1)):
              self.obstacle[p[0]+dir[i]][p[1]+dir[j]] = self.obstacle[p[0]][p[1]] + 1
              lst.append((p[0]+dir[i],p[1]+dir[j]))
          except :
            print("error at ", p[1]+dir[j], p[0] + dir[i], self.dim[0],  self.dim[1])      
      
class vehicle:
  def __init__(self, ID, Turning_Radius, angle : int or None,  startingLocation : ):
    self.ID = ID
    self.Turning_Radius = Turning_Radius
    self.startLocation = None 
  
  def location(self, startingLocation, endLocation):
    self.stating_Location = startingLocation
    self.end_location = endLocation

  def hurestic(self):
    


