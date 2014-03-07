# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [ [0, 1, 1, 0, 0, 0],
         [0, 1, 1, 0, 0, 0],
         [0, 1, 0, 0, 1, 0],
         [0, 1, 0, 1, 0, 0],
         [0, 0, 0, 1, 0, 0] ]

heuristic = [[9, 8, 7, 6, 5, 4],
            [8, 7, 6, 5, 4, 3],
            [7, 6, 5, 4, 3, 2],
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

success_prob= 0.5
failure_prob = (1.0 - success_prob)/2.0  # Probability(stepping_left) = prob(steeping_right) = failure_prob
collision_cost = 100
cost_step = 1

def compute_value():
    """
    Returns a grid of values. Value is defined as the minimum number
    of moves required to get from a cell to the goal.
    
    If it is impossible to reach the goal from a cell, the cell
    will be assigned with a value of 99. 
    """
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    
    change = True
    while change:   #continuous propogation 
        change = False  #in order to keep iterating, a change has to occur below

        for x in range(len(grid)):
            for y in range(len(grid[0])):

                # Are we in the goal cell?
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True

                # If it's not a goal cell, but not an obstacle, 
                # we go through and update the corresponding value position!
                elif grid[x][y] == 0:
                    
                    #go through all the actions, first finding a potential next state
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        # Are the actions valid within the grid, and is the grid cell navigable?
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:

                            # new value is the value of the future grid cell, plus the cost_step per step
                            v2 = value[x2][y2] + cost_step

                            # if the potential value is smaller than where we're at, assign it
                            if v2 < value[x][y]:
                                change = True       # we've made a change, so we have to repeat
                                value[x][y] = v2

    for i in range(len(value)):
        print value[i]

def optimum_policy():
    """
    Returns a grid which show the optimun policy for robot motion.
    This means there should be an optimum directions associated
    with each navigable cell. 

    Un-naviagable cells contain an empty string with a space

    The goal is marked as '*'
    """
    # We have all the information for how we reached the goal
    # now let's represent it as an optimal policy
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = "*"

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost_step

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                                #assign the character in delta_name that coresponds to the optimal action we're taking
                                policy[x][y] = delta_name[a]                           


    #print the final policy table
    for i in range(len(policy)):
        print policy[i]

    return policy # Make sure your function returns the expected grid.

    



def search():
    """
    Implements and A-star search to find an optimal
    path through the world
    """
    # Create a new array matching the grid that tracks closed positions with 0's
    # (closed being those that we haven't yet opened!)
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    
    #every opened position becomes a 1... starting with init
    closed[init[0]][init[1]] = 1 

    # Make a grid to track expansions
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand_count = 0

    #Make a grid to track our software's chosen path
    # We can store an index to memorize what action we took to get to a certain cell
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]


    x = init[0]
    y = init[1]
    g = 0   # distance traversed
    h = heuristic[x][y]   # starting heuristic value
    f = g + h

    # Initialize an open list, starting with our first g, x, and y
    open = [[f, g, h, x, y]]

    found = False    # flag that is set when search completes
    resign = False   # flag set if we can't find the goal

    print 'initial open list:'
    for i in range(len(open)):
        print '  ', open[i]
    print '----'

    # Begin ze search!
    while not found and not resign:

        #check if we still have elements on the open list
        if len(open) == 0:
            resign = True
            print "fail"
        else:
            open.sort()         # sort according to f
            next = open.pop(0)  # pop the smallest value

            x = next[3]
            y = next[4]
            g = next[1]     # we'll compute f and h later
            
            expand[x][y] = expand_count
            expand_count += 1

            if x == goal[0] and y == goal[1]:
                found = True
                print next
                print "Search successful!"
                break

            else:
                # expand winning element and add to new open list
                
                # first find our candidate in adjacent positions
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]

                    # Does x2 and y2 fall within the grid?
                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]): 
                        # Have x2 and y2 been checked? 
                        # Also, is the space unblocked on the grid?
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost_step
                            h2 = heuristic[x2][y2]
                            f2 = g2 + h2
                            
                            # Add our new values to the 'open' stack... this is how
                            # we pick the best (i.e., min) value in the next pass!!!
                            open.append([f2, g2, h2, x2, y2])
                            closed[x2][y2] = 1
                            
                            # i here is associated with the successor state, and so its marking corresponds
                            # to the optimal action
                            action[x2][y2] = i   
                            
                            #print 'appended list item:'
                            #print [g2, x2, y2]


    # We have all the information for how we reached the goal
    # now let's represent it as an optimal policy
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    x = goal[0]
    y = goal[1]
    policy[x][y] = '*'

    while x != init[0] or y != init[1]:
        x2 = x - delta[ action[x][y] ][0]   # find the proper x position in delta correspondng with the action index
        y2 = y - delta[ action[x][y] ][1]   # find the proper y position in delta correspondng with the action index
        policy[x2][y2] = delta_name[action[x][y]]   # mark the policy field to correspond with the proper delta symbol
        x = x2  #recurse!
        y = y2

    #print the final policy table
    for i in range(len(policy)):
        print policy[i]


    
    return expand # you should RETURN your result


#expand = search()
#for l in range(len(expand)):
#    print expand[l]




def stochastic_value():
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = "*"

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        
                        v2 = cost_step

                        # explore the different action outcomes
                        for i in range(-1, 2):

                            a2 = (a + i) % len(delta)
                            x2 = x + delta[a2][0]
                            y2 = y + delta[a2][1]

                            if i == 0:
                                p2 = success_prob
                            else:
                                p2 = (1.0 - success_prob) / 2.0

                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 += p2 * value[x2][y2]
                            else:
                                v2 += p2 * collision_cost

                        if v2 < value[x][y]:
                            change = True
                            value[x][y] = v2
                            policy[x][y] = delta_name[a]

    
    return value, policy

print stochastic_value()






















