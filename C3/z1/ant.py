import numpy as np
import operator

def norm(weights):
    s = sum(weights)
    return list(map(lambda x : x/s, weights))


class City(object):
    def __init__(self, coordinate, neighbours):
        self.coordinate = coordinate
        self.neighbours = neighbours

    def dist(self, city):
        return np.linalg.norm(np.subtract(self.coordinate, city.coordinate))

c = []
c.append(City((0,0), [1,2,3])) #c0
c.append(City((2,3), [0,2,3,4])) #c1
c.append(City((1,4), [0,1,4])) #c2
c.append(City((6,2), [0,1,4])) #c3
c.append(City((6,7), [1,2,3])) #c4

f = {}
f[(0,1)] = 1
f[(0,2)] = 1
f[(0,3)] = 1
f[(1,2)] = 1
f[(1,3)] = 1
f[(1,4)] = 1
f[(2,4)] = 1
f[(3,4)] = 1

class Ant(object):
    def __init__(self, start_city_index, end_city_index):
        self.path_length = 0.0
        self.pos = start_city_index
        self.dest = end_city_index
        self.visited = [self.pos]

    def turn(self):
        if self.pos == self.dest:
            return

        movs = list(filter(lambda x : x not in self.visited, c[self.pos].neighbours))
        if movs:
            next_edges = list(map(lambda x: (self.pos,x) if x>self.pos else (x,self.pos), movs))

            weights = norm([f[x] for x in next_edges])
            prev = self.pos
            self.pos = np.random.choice(movs, p=weights)
            self.visited.append(self.pos)
            self.path_length += c[prev].dist(c[self.pos])

    def update_patch(self):
        if self.pos != self.dest:
            return
        val = 1/self.path_length
        edges = list(zip([0]+self.visited, self.visited+[0]))[1:-1]
        edges = list(map(lambda x : x if x[0]<x[1] else (x[1],x[0]), edges))
        for e in edges:
            f[e] += val

def steam(p):
    for x in f:
        f[x] *= p


rep = 1000
g = 6
p = 0.9999
for i in range(rep):
    m=[]
    m.append(Ant(0,4))
    m.append(Ant(1,4))
    m.append(Ant(2,4))
    m.append(Ant(3,4))

    for g in range(g):
        for a in m:
            a.turn()

    steam(p)
    for a in m:
        a.update_patch()

print(sorted(f.items(), key=operator.itemgetter(1)))

