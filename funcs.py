from .resources import np

def multi(a, b):
  met = np.multiply(a,b)
  sum = 0
  for i in range(len(met)):
    for val in met[i]:
      sum+=val
  return sum

def sub_array(a, i,j, conv):
  b = [[-1 for i in range(conv)] for j in range(conv)]
  for k in range(i,i+conv):
    for l in range(j, j+conv):
      b[k-i][l-j]=a[k][l]
  return b

# Convert the values of dem to numbers as the input is in string

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
