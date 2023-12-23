from .resources import np, plt, noise, gaussian_filter


if os.path.exists('DEM.txt'):
    print('The file exists!')
else:
    print("This doesn't exist")

def plot_dem(dem):
    fig = plt.figure()
    dem_temp = dem
    ax = fig.add_subplot(111, projection='3d')
    rows, cols = np.array(dem).shape
    x = np.arange(0, cols, 1)
    y = np.arange(0, rows, 1)
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, dem, cmap='terrain')
    plt.show()

def generate_smooth_dem(rows, cols, scale=100.0, octaves=0.3, persistence=0.5, lacunarity=0.0, seed=None, smoothness=3.0, new_min=0, new_max=100):
    world = np.zeros((rows, cols))

    for i in range(rows):
        for j in range(cols):
            world[i][j] = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)

    min_value = np.min(world)
    max_value = np.max(world)
    world = (world - min_value) / (max_value - min_value)  # Normalize to range [0, 1]

    # Apply Gaussian filter for increased smoothness
    world_smooth = gaussian_filter(world, sigma=smoothness)

    # Scale to the new range [new_min, new_max]
    world_smooth_scaled = (world_smooth * (new_max - new_min)) + new_min

    return world_smooth_scaled
    # return world_smooth_scaled



# Example usage
rows = 200
cols = 200
scale = 30
# octaves = 2
# persistence = 0.5
# lacunarity = 0
# seed = 6
octaves = 2
persistence = 1
lacunarity = 2.0
seed = 4
smoothness = 5
new_min = -5
new_max = 4 # Adjust the new maximum height

smooth_dem = generate_smooth_dem(rows, cols, scale, octaves, persistence, lacunarity, seed, smoothness, new_min, new_max)
print(smooth_dem)
plot_dem(smooth_dem)   



# print(smooth_dem)
  

file.close()



import random
mn = np.min(dem)
mx = np.max(dem)
file = open("DEM.txt", 'w')
for i in range(100):
  dem[random.randint(0, len(dem)-1)][random.randint(0, len(dem[0])-1)] = random.uniform(mn, mx)

for i in range(len(dem)):
  dem[i] = dem[i][:-1]
dem = dem[:][:-1]
# This to remove extra 'n' at last

# @title Default title text
def multi(a, b):
  # print(a[0][0])
  met = np.multiply(a,b)
  # print(a[0][0], met[0][0])
  # print(met)
  sum = 0
  for i in range(len(met)):
    for val in met[i]:
      sum+=val
  # print(sum , a/[0][0])
  return sum

def sub_array(a, i,j, conv):
  b = [[-1 for i in range(conv)] for j in range(conv)]
  for k in range(i,i+conv):
    for l in range(j, j+conv):
      b[k-i][l-j]=a[k][l]

  # print(b)
  return b

# Convert the values of dem to numbers as the input is in string
for i in range(len(dem)):
  for j in range(len(dem[0])):
    dem[i][j] = float(dem[i][j])

from copy import copy, deepcopy

def find_conv(dem, conv= 20):
  val = 1/(1.0*conv*conv)
  m = [[1/(conv*conv) for i in range(conv)] for j in range(conv)]
  dem_temp = deepcopy(dem)
  for i in range(len(dem) - int(conv)):
    for j in range(len(dem[0]) - int(conv)):
      dem_temp[i+int(conv/2)][j+int(conv/2)] = multi(sub_array(dem, i, j, int(conv)), m)
  return dem_temp    
  plot_dem(np.array(dem_temp))


def st_dev(dem, dem_temp):
  dem_standard = deepcopy(dem_temp)
  for i in range(len(dem)):
    for j in range(len(dem[0])):
      dem_standard[i][j] = (dem[i][j] - dem_temp[i][j])**2
  return dem_standard
  plot_dem(np.array(dem_standard))

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
    for i in range(len(dem)):
      for j in range(len(dem[0])):
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
  def __init__(self, ID, Turning_Radius):
    self.ID = ID
    self.tr = Turning_Radius

  def calculate_hurestic(self, map):
                  

map1 = map(dem, obstacle)

