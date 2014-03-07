from math import *

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

# ------------------------------------------------
# smooth coordinates
#

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]

    #as long as change >= tolerance, we keep running gradient descent
    change = tolerance
    while change >= tolerance:
        change = 0.0
        for i in range(1, len(newpath)-1):
            for j in range(len(newpath[0])):
                aux = newpath[i][j]     # use aux to track the change
                newpath[i][j] += weight_data * (path[i][j] - newpath[i][j])
                newpath[i][j] += weight_smooth * ( (newpath[i+1][j] + newpath[i-1][j]) - (2.0 * newpath[i][j]) )
                change += abs(aux - newpath[i][j])
                   
    
    
    return newpath # Leave this line for the grader!

# feel free to leave this and the following lines if you want to print.
newpath = smooth(path)

for i in range(len(path)):
    print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'





############ Cyclic smoothing #################

def cyc_smooth(path, weight_data = 0.1, weight_smooth = 0.1, tolerance = 0.00001):

    # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]

    #as long as change >= tolerance, we keep running gradient descent
    change = tolerance
    path_size = len(newpath)
    while change >= tolerance:
        change = 0.0
        for i in range(len(newpath)):
            for j in range(len(newpath[0])):
                aux = newpath[i][j]     # use aux to track the change
                newpath[i][j] += weight_data * (path[i][j] - newpath[i][j])
                newpath[i][j] += weight_smooth * ( (newpath[ (i+1) % path_size ][j] + newpath[ (i-1) % path_size ][j]) - (2.0 * newpath[i][j]) )
                change += abs(aux - newpath[i][j])
    
    return newpath




def constrained_cyc_smooth(path, weight_data = 0.1, weight_smooth = 0.1, tolerance = 0.00001):


 # Make a deep copy of path into newpath
    newpath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]

    #as long as change >= tolerance, we keep running gradient descent
    change = tolerance
    path_size = len(newpath)
    while change >= tolerance:
        change = 0.0
        for i in range(len(newpath)):
            for j in range(len(newpath[0])):
                if not fix[i]:
                    aux = newpath[i][j]     # use aux to track the change
                    newpath[i][j] += weight_data * (path[i][j] - newpath[i][j])

                    newpath[i][j] += weight_smooth * ( (newpath[ (i+1) % path_size ][j]
                                                      + newpath[ (i-1) % path_size ][j])
                                                      - (2.0 * newpath[i][j]) )

                    newpath[i][j] += 0.5 * weight_smooth * ( (2.0 * newpath[ (i-1) % path_size ][j]) 
                                                              - (newpath[ (i-2) % path_size ][j])
                                                              - (newpath[i][j]) )
                    newpath[i][j] += 0.5 * weight_smooth * ( (2.0 * newpath[ (i+1) % path_size ][j]) 
                                                              - (newpath[ (i+2) % path_size ][j])
                                                              - (newpath[i][j]) )

                    change += abs(aux - newpath[i][j])
    
    return newpath





