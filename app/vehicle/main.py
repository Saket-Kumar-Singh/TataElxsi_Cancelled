import location 
import math
import socket 
from communication import *
THRESHHOLD = 20
ID = 1

def read_node():    
    f = open("path.txt", "r")
    p = f.read()
    p = p.split(" ")
    nodes = []
    for k in p:
        x = k.split(",")
        t1 = int(x[0])
        t2 = int(x[1])
        nodes.append((t1, t2))

def request_new_nodes(x, y):
    print(f"will call new path starting from {x},{y}")
    f = open("path.txt", "w")
    f.write("0,0 1,1 2,2 3,3 4,4 5,5")
    f.close()

def dist(a, b, c, d):
    return math.sqrt((a-c)**2 + (b - d)**2)

def find_closest(x, y, nodes):
    closest = 1e9+7
    x1, y1
    for p in nodes:
        if dist(x, y, p[0], p[1]) < closest:
            closest = dist(x, y, p[0], p[1])
            x1 = p[0]
            y1 = p[1]
    print("The closest node is ")
    if(closest >= THRESHHOLD):
        return None        
    return (x1, y1)

def make_vehicle(k):
    ...
    return False




if __name__ == "__main__":
    k = socket.gethostname()
    if not check_present(k):
        k = make_vehicle(k)
        
    else:
        k = check_present(k) 
    # exec()
    # while(True):
    #     x,y = get_location()
    #     try:
    #         nodes = read_node()
    #     except:
    #         request_new_nodes(x, y)
    #         nodes = read_node()

    #     k = find_closest(x, y, nodes)
    #     if not k:
    #         request_new_nodes(x, y)
    #         nodes  = read_node()    
    #         x1, y1 = x, y
    #     else:
    #         x1, y1 = k[0], k[1]
        
    #     ind = 0
    #     while(dist(x1, y1, ))       