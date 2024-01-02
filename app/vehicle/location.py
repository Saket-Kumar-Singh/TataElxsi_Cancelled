import numpy as np
from datetime import datetime 
import time
import matplotlib.pyplot as plt
def get_data():
    return [4, 5, 6, 7, 8, 9]

def get_position():
    return [10, 11, 12]

def get_location(x,P, las_reached):
    curr_time = datetime.now()
    timedelta =  curr_time - las_reached
    t = timedelta.total_seconds() 
    # t = (las_reached.second * 10**6 + las_reached.microseconds - curr_time.second * 10 ** 6 - curr_time + ) / (10**6)
    print("generating location through kalman filter")
    # result from imu = [x, y, z, vx, vy, vz, az, ay, az] 
    # v = imu[3:6] (1X3)
    # a = imu[6:9] (1X3)
    lst = [[0.0 for i in range(9)] for j in range(9)]
    for i in range(9):
        lst[i][i] = 1
    for i in range(3):
        lst[3+i][i] = t
        lst[6+i][i] = 0.5*t*t
        lst[6+i][3+i] = t        
    # t = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0], [0, t, 0], [0, 0, t]])
    F = np.array(lst)
    l = [1, 2, 3]
    if type(x) != type(np.array(l)):
        x = np.array(x)

    Q = np.eye(9) 
    H = np.eye(9)   
    R = np.eye(9)

    imu = get_data()
    yk = get_position()
    yk = yk + imu
    # print(yk)
    
    xk_ = F @ x
    Pk_ = F @ P @ F.T + Q
    Kk = Pk_ @ H.T @ np.linalg.inv((H @ Pk_ @ H.T + R))
    xk = xk_ + Kk @ (yk - H @ xk_)
    Pk = (np.eye(9) - Kk @ H) @ Pk_
    curr_time = datetime.now()
    return xk, Pk, curr_time

    # except :
    #     # print("error")
    #     return 0, 0, datetime.now()
    # yk = imu[:3]


if __name__ == "__main__":
    # x,y = get_location()
    x = np.eye(9)
    P = np.eye(9)
    t = datetime.now()
    x_pos = []
    y_pos = []
    t_pos = []
    for i in range(5):
        x, P, t = get_location(x, P, t)
        time.sleep(1)
        x_pos.append(x[0])
        y_pos.append(x[1])
        t_pos.append(t)
    
    fig1 = plt.plot(t_pos, x_pos, label = "X Pos")
    fig2 = plt.plot(t_pos, y_pos, label = "Y Pos")

        # print("The value of x is ", x)        