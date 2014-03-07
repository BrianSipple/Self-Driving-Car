
 
from math import *
import random


# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift: 
    #	sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift
        
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance, 
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)

############## ADD / MODIFY CODE BELOW ####################
    
# ------------------------------------------------------------------------
#
# run - does a single control run


def run(params, printflag=False):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 100
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree bias, this will be added in by the move function, you do not need to add it below!
    
    crosstrack_error = myrobot.y

    for i in range(N * 2):
        differential_ct = myrobot.y - crosstrack_error  #momentary CTE - previous CTE
        crosstrack_error = myrobot.y
        int_crosstrack_error += crosstrack_error
        steer = (-params[0] * crosstrack_error) - (params[1] * differential_ct) - (params[2] * int_crosstrack_error)
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += (crosstrack_error ** 2)
        if printflag:
            print myrobot, steer
        return err / float(N)


def twiddle(tol = 0.0001): #Make this tolerance bigger if you are timing out!            

    n_params = 3
    params = [0.0 for i in range(n_params)]
    dparams = [1.0 for i in range(n_params)]       #delta params
    
    best_err = run(params)
    n = 0   # counter

    while sum(dparams) > tol:
        for i in range(len(params)):
            params[i] += dparams[i]
            err = run(params)   
            if err < best_err:
                best_err = err
                dparams[i] *= 1.1     # If we're successful, keep the new error, and increase the delta params

            else:                # If we're not successful above, decrement the delta params and try again
                params[i] -= 2.0 * dparams[i] 
                err = run(params)
                if err < best_err:
                    best_err = err
                    dparams[i] *= 1.1
                else:           
                    params[i] += dparams[i]  #If we're still not minimizing error, increase params by dp value and decrease dp for next pass
                    dparams[i] *= 0.9

        n += 1
        print "Twiddle #", n, params, ' -> ', best_err
    print ' '
    return run(params)


twiddle()

################################## Cyclic run ###########################


   
def cte(self, radius):
    """
    Here, we'd like to measure cte as the distance from the robot
    to the center of the course
    """
    if self.x < radius: #left side of the course
        cte = sqrt((self.x - radius) ** 2 + (self.y - radius) ** 2) - radius
    elif self.x > 3.0 * radius: #more than 3 times over to the right
        cte = sqrt((self.x - 3.0 * radius) ** 2 + (self.y - radius) ** 2) - radius

    # now we account for the straightaways
    elif self.y > radius: #top straightaway
        cte = self.y - 2.0 * radius 

    else:   #bottom straightaway
        cte =  - self.y 
    return cte


def cyc_run(params, , radius=25, printflag=False):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    err = 0.0
    int_crosstrack_error = 0.0
    N = 100
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree bias, this will be added in by the move function, you do not need to add it below!
    
    crosstrack_error = myrobot.y

    for i in range(N * 2):
        differential_ct = myrobot.y - crosstrack_error  #momentary CTE - previous CTE
        crosstrack_error = myrobot.y
        int_crosstrack_error += crosstrack_error
        steer = (-params[0] * crosstrack_error) - (params[1] * differential_ct) - (params[2] * int_crosstrack_error)
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += (crosstrack_error ** 2)
        if printflag:
            print myrobot, steer
        return err / float(N)


