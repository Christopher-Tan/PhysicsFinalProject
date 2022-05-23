import math
#Constants
g = 10
class Pendulum:
    def __init__(self):
        self.start = Node(0,0)
        self.end = self.start
    def add_node(self, mass, length):
        new_node = Node(mass, length, self.end)
        self.end.n = length, new_node
        self.end = new_node
        self.start.max_force()
        self.start.force()
    def elapse(self, dt):
        self.start.force()
        self.start.elapse(dt)
        self.end.coords()
        
class Node:
    #Update values
    def coords(self):
        if (self.p[1] != None):
            self.p[1].coords()
            self.c[0] = self.p[1].c[0] + self.p[0] * math.cos(self.x)
            self.c[1] = self.p[1].c[1] + self.p[0] * math.sin(self.x)
    def max_force(self):
        if (self.n[1] != None):
            self.n[1].max_force()
            self.f_max = self.n[1].f_max + self.m * g
    def force(self):
        if (self.n[1] != None):
            self.n[1].force()
            self.f = [self.m * g * math.sin(self.x-math.pi) + self.n[1].f[0] * math.cos(self.n[1].x-self.x), self.m * g * math.cos(self.x-math.pi) + self.n[1].f[0] * math.sin(self.n[1].x-self.x)]
        else:
            self.f = [self.m * g * math.sin(self.x-math.pi), self.m * g * math.cos(self.x-math.pi)]
    def elapse(self, dt):
        if (self.n[1] != None):
            a = self.f[1] / (self.m * self.p[0]) if self.p[0] != 0 else 0
            self.v += a * dt
            self.x += self.v * dt
            self.n[1].elapse(dt)

    
    def __init__(self, mass, length, previous = None):
        self.m = mass
        #Angular
        self.x = 0
        self.v = 0
        self.f_max = mass * g
        #Link
        self.p = [length, previous]
        self.n = [0, None]
        #Cartesian
        self.c = [0,0]
        self.coords()
        #Forces
        self.f = [0,0] #Normal, Tangential

a = Pendulum()