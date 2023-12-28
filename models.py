from .utils import find_conv, st_dev, abs
from .resources import np, noise, gaussian_filter, math, PQ
from pydantic import BaseModel, EmailStr

class Location(BaseModel):
  x : int
  y : int
  angle : int or None 

class map: 
  def __init__(self, dem, obstacle, width = 6):
    self.dem = dem
    self.obstacle = obstacle
    self.dem_temp = find_conv(dem, conv = 20)
    self.dem_st_dev = st_dev(dem, self.dem_temp)
    self.add_obstacles()
    self.dim = np.shape(np.array(self.obstacle)) 
    self.bfs()   
    self.make_penalty(width)
    self.path = [[-1 for i in range(self.dim[0])] for j in range(self.dim[1])]
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

  def make_penalty(self, width):
    for i in range(self.dim[0]):
      for j in range(self.dim[1]):
        self.obstacle[i][j] = self.func(self.obstacle[i][j], width) 

  def func(self, x, width):
    if(x <= width):
      return 100
    else:
      return 100*math.e**(-1*((x-width)**2))

  def cost(self, x, y, x1, y1):
    val = 0.0
    for i in range(x, x1+1):
      for j in range(y, y1+1):
        val += self.dem[i][j]
    val = val/(abs((x-x1)*(y - y1)))
    ans = 0.0
    for i in range(x, x1 + 1):
      for j in range(y, y1+1):
        ans+=((self.dem[i][j] - val)**2)
    return ans/(abs((x1 - x)*(y1 - y)))    

class vehicle:
  def __init__(self, ID):
    self.ID = ID
  
  def location(self, startingLocation, endLocation):
    self.stating_location = startingLocation
    self.end_location = endLocation

  def a_star(self, map, step_size = 20):
    x = self.stating_location[0]
    y = self.stating_location[1]
    x1 = self.end_location[0]
    y1 = self.end_location[1]

    self.path = []
    self.path.append((x, y))
    dir = [-1*step_size, 0, step_size]
    pq = PQ()
    pq.put((0, x, y))
    while not pq.empty() and (x != x1 and y != y1):
      cst, x, y = pq.get()
      for i in range(3):
        for j in range(3):
          if(x + dir[i] < self.dim[0] and x + dir[i] >= 0) and (y+ dir[j] < self.dim[1] and y + dir[j] >= 0):
            if self.path[x + dir[i]][y + dir[j]] != -1:
              val = cst + map.cost(x, y, x + dir[i], y + dir[j])
              self.path[x + dir[i]][y + dir[j]] = val
              pq.put((val, x + dir[i] , y + dir[j])) 



