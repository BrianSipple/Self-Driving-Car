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


