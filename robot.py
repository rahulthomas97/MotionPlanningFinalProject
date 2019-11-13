#!/usr/bin/env python
from environments import *
import random
import matplotlib
import copy
from lidar import LidarSensor

class Robot:
    def __init__(self, sensor_configuration, map_file, actions):
        self.GridMap = GridMap(map_file)
        self.truth_position = self.GridMap.init_pos
        self.path_taken = []
        self.rows = self.GridMap.rows
        self.columns = self.GridMap.cols
        self.probability_map = self.GridMap.probability_map
        self.actions = actions
        self.sensor_config = LidarSensor(sensor_configuration,self.GridMap)
        self.gauss_3x3 = np.array(([1, 2, 1],[2, 4, 2],[1, 2, 1]))/16.0 #3x3 gaussian kernel

    def transition_function(self, action):
        '''
        returns possible states transitioned to.
        '''
        return

    def queue_sensors(self,state=None):
        '''
        Sensor Reading, u->blocked, r->open, etc.
        returns distance to obsticle for sensor obsticles
        '''
        if(state):
            return self.sensor_config.queue_sensors(state)
        else:
            return self.sensor_config.queue_sensors(self.truth_position)

    def get_possible_states(self, sensor_reading):
        '''
        Loop over every state with non-zero probabilities, get it's sensor
        reading, and see if it matches our current one.
        '''
        possible_states = []
        for r in range(self.rows):
            for c in range(self.columns):
                if(self.probability_map[r,c]):
                    if(self.queue_sensors((r,c,0)) == sensor_reading):
                        possible_states.append((r,c,0))

        return possible_states

    def distribution_from_possible_states(self,states):
        '''
        Get the probability distriubtion from the possible states
        '''
        return

    def update_prob_map(self, possible_states=None, action=None):
        '''
        Use the distribution from possible states and the current probability map
        to get the new distribution of where we are
        '''
        if(possible_states):
            #We could add a gaussian kernel at each of these states?
            probability_of_possible_states = 1.0 / (len(possible_states))
            likelihood = np.zeros(self.probability_map.shape)
            for state in possible_states:
                likelihood[state[0:2]] = probability_of_possible_states
            #Bayes Rule...
            posterior = likelihood * self.probability_map
            #Normalize the resulting distribution
            posterior /= np.sum(posterior)
            #The posterior now becomes the prior (our self.probability_map)
            self.probability_map = copy.copy(posterior)
        if(action):

        return

    def get_prob_from_transition(self):
        '''
        When we take an action, uncertainty will grow because we are now
        less sure of our state. We need to update our probability map
        using the possible states from our transition function...
        '''
        return

    def display_probability_map(self):
        plt.figure()
        imgplot = plt.imshow(self.probability_map)
        # Set interpolation to nearest to create sharp boundaries
        imgplot.set_interpolation('nearest')
        # Set color map to diverging style for contrast
        # imgplot1.set_cmap('gray')
        imgplot.set_cmap('Spectral')

        plt.show()

    def display_traveled_map(self):
        return

    def random_movement(self):
        rand_act =  random.choice(self.actions)
        #Keep track of where we go...
        self.path_taken.append(self.truth_position)
        self.truth_position = self.GridMap.transition(self.truth_position, rand_act)
        return rand_act
