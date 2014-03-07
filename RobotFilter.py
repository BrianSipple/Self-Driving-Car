# In this exercise, please run your previous code twice.
# Please only modify the indicated area below!

from math import *
import random

max_steering_angle = pi / 4.0 # You do not need to use this value, but keep in mind the limitations of a real car.
bearing_noise = 0.1 # Noise parameter: should be included in sense function.
steering_noise = 0.1 # Noise parameter: should be included in move function.
distance_noise = 5.0 # Noise parameter: should be included in move function.

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks in (y, x) format.
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"

class robot:
    def __init__(self, length = 20.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
    
    
    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
    
    
    def sense(self, add_noise = 1):
        """
        Obtains bearings from positions
        """
        Z = []
        for l in range(len(landmarks)):
            
            # atan2 is the function we use for computing the local angle 
            # of the landmark relative to the robot coordinate
            bearing = atan2( (landmarks[l][0] - self.y), (landmarks[l][1] - self.x) ) - self.orientation
            
            if add_noise:
                bearing += random.gauss(0.0, self.bearing_noise)
            bearing %= 2.0 * pi
            
            Z.append(bearing)

        return Z

    
    
    def move(self, motion, tolerance = 0.001): # Do not change the name of this function
            """
            Recieves motions as [steering_angle, distance]
            """

            steering_angle = float(motion[0])
            distance = float(motion[1])
        
            # validation
            if abs(steering_angle) > max_steering_angle:
                raise ValueError, "Exceeding max steering angle!"
            if distance < 0.0:
                raise ValueError, 'Moving backwards is not allowed!'
     
            # apply noise
            steering_angle2 = random.gauss(steering_angle, self.steering_noise)   # mean is steering angle, sigma is noise
            distance2 = random.gauss(distance, self.distance_noise)

            
            turning_angle = (distance2 / self.length) * tan(steering_angle2)
            
            
            if abs(turning_angle) >= tolerance:
                # approximate bicycle model for motion
                radius = distance2/turning_angle
                cx = self.x - (sin(self.orientation) * radius)
                cy = self.y + (cos(self.orientation) * radius)
                
                new_x = cx + (sin(self.orientation + turning_angle) * radius)
                new_y = cy - (cos(self.orientation + turning_angle) * radius)
                new_orientation = (self.orientation + turning_angle) % (pi*2)
            
            else:
                # approximate by straight-line motion
                new_x = self.x + (distance2 * cos(self.orientation))
                new_y = self.y + (distance2 * sin(self.orientation))
                new_orientation = (self.orientation + turning_angle) % (pi*2)
            

            #make the new robot copy
            result = robot(self.length)
            result.set(new_x, new_y, new_orientation)
            result.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)
            
            return result # make sure your move function returns an instance
                          # of the robot class with the correct coordinates.
        
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurements):
        
        # calculates how likely a measurement should be
        predicted_measurements = self.sense(0)

        #compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            # In case the difference falls outside of [-pi,+pi]... so we bring it back to 
            # the the smallest possible value in the cyclic space between
            # 
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
        
            #update Gaussian
            error *= (exp(- (error_bearing**2) / (self.bearing_noise ** 2) / 2.0) /
                sqrt(2.0 * pi * (self.bearing_noise ** 2)))

        return error
    
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]


def generate_ground_truth(motions):

    myrobot = robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
    #print 'Robot:   ', myrobot
    return [myrobot, Z]


# The following code prints the measurements associated
# with generate_ground_truth
#

def print_measurements(Z):

    T = len(Z)

    print 'measurements = [[%.8s, %.8s, %.8s, %.8s],' % \
        (str(Z[0][0]), str(Z[0][1]), str(Z[0][2]), str(Z[0][3]))
    for t in range(1,T-1):
        print '                [%.8s, %.8s, %.8s, %.8s],' % \
            (str(Z[t][0]), str(Z[t][1]), str(Z[t][2]), str(Z[t][3]))
    print '                [%.8s, %.8s, %.8s, %.8s]]' % \
        (str(Z[T-1][0]), str(Z[T-1][1]), str(Z[T-1][2]), str(Z[T-1][3]))



# --------
#
# The following code checks to see if your particle filter
# localizes the robot to within the desired tolerances
# of the true position. The tolerances are defined at the top.
#

def check_output(final_robot, estimated_position):

    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct



def particle_filter(motions, measurements, N=500): # I know it's tempting, but don't change N!
    # --------
    #
    # Make particles
    # 

    p = []
    for i in range(N):
        r = robot()
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        p.append(r)

    # --------
    #
    # Update particles
    #     

    for t in range(len(motions)):
    
     # update p with a distribution of all new robot particle states after a move
        p2 = []
        for i in range(N):
            p2.append(p[i].move(motions[t]))
        p = p2

        #probability (importance) weights of our initial robot's measurement (Z) corresponding 
        #to each state particle in p
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(measurements[t]))

        #awesome resampling wheel
        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            # Decrease beta by the w[index] value, then update the index until
            # its w[index] value exceeds beta. 
            # Append p3 with the p[index] corresponding to the index
            # This ensures a random particles are chosen, BUT that particles with a higher
            # importance weight are chosen more frequently!
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        
         
        #final update of p... basically with all of the particles that our 
        #kick-ass resampling wheel decided to keep. 
        p = p3
        
        #comparison
    return get_position(p)


#################################################     TESTING     ############################################################

## TEST CASES:
## 
##1) Calling the particle_filter function with the following
##    motions and measurements should return a [x,y,orientation]
##    vector near [x=93.476 y=75.186 orient=5.2664], that is, the
##    robot's true location.
##
motions = [[2. * pi / 10, 20.] for row in range(8)]
measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
                [3.510067, 2.916300, 2.146394, 1.598332],
                [2.972469, 2.407489, 1.588474, 1.611094],
                [1.906178, 1.193329, 0.619356, 0.807930],
                [1.352825, 0.662233, 0.144927, 0.799090],
                [0.856150, 0.214590, 5.651497, 1.062401],
                [0.194460, 5.660382, 4.761072, 2.471682],
                [5.717342, 4.736780, 3.909599, 2.342536]]

print particle_filter(motions, measurements)

## 2) You can generate your own test cases by generating
##    measurements using the generate_ground_truth function.
##    It will print the robot's last location when calling it.
##
##
##number_of_iterations = 6
##motions = [[2. * pi / 20, 12.] for row in range(number_of_iterations)]
##
##x = generate_ground_truth(motions)
##final_robot = x[0]
##measurements = x[1]
##estimated_position = particle_filter(motions, measurements)
##print_measurements(measurements)
##print 'Ground truth:    ', final_robot
##print 'Particle filter: ', estimated_position
##print 'Code check:      ', check_output(final_robot, estimated_position)







