colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

# colors=[['green','green','green'],
          # ['green','red','red'],
          # ['green','green','green']]
# measurements=['red','red']
# motions=[[0,0],[0,1]]
# sensor_right = 1.0
# p_move = 0.5

def showf(p):
    for i in range(len(p)):
        for c in p[i]:
            print "%.6f " % (c),
        print
    print "=========="

def showf(p):
    pass

def uniform(grid):
    p = []
    n = len(grid) * len(grid[0])
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            row.append(1./n)
        p.append(row)
    return p

def sense(p, Z):
    q = []
    for i in range(len(p)):
        row = []
        for j in range(len(p[i])):
            if (Z == colors[i][j]):
                q_pZ = sensor_right
            else:
                q_pZ = 1 - sensor_right
            row.append(p[i][j] * q_pZ)
        q.append(row)
    s = 0.0
    for i in range(len(q)):
        for j in range(len(q[i])):
            s = s + q[i][j]
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = q[i][j] / s
    return q

def move(p, U):
    q = []
    (dy,dx) = (U[0],U[1])
    assert((dy==0) or (dx==0))
    for i in range(len(p)):
        row = []
        for j in range(len(p[i])):
            y = (i-dy) % len(p)
            x = (j-dx) % len(p[i])
            s = (p[y][x] * p_move) + (p[i][j] * (1-p_move))
            row.append(s)
        q.append(row)
    return q

p = uniform(colors)
for i in range(len(motions)):
    showf(p)
    p = move(p,motions[i])
    p = sense(p,measurements[i])




#Your probability array must be printed
#with the following code.

show(p)
showf(p)


