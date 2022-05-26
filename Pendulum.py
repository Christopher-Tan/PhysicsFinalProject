import math
import time
import matplotlib.pyplot as plt
import random

def sum(v1,v2):
    x = v1[0] * math.cos(v1[1]) + v2[0] * math.cos(v2[1])
    y = v1[0] * math.sin(v1[1]) + v2[0] * math.sin(v2[1])
    return [math.sqrt(x ** 2 + y ** 2), math.atan2(y, x)] #magnitude, angle
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
        self.end.acceleration()
        self.start.elapse(dt)
        self.end.coords()
    def coords(self):
        i = self.start
        c = []
        while (i != None):
            c.append(i.c)
            i = i.n[1]
        return c
        
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
    def acceleration(self):
        if (self.p[1] != None):
            self.p[1].acceleration()
            try:
                self.a = sum(self.p[1].a,[self.f[1]/self.m * math.sin(self.n[1].x-self.x), self.n[1].x])
            except:
                self.a = [0,0]
        else:
            self.a = [0,0]
    def elapse(self, dt):
        if (self.p[1] == None):
            a = 0
        elif (self.p[1].m == 0):
            a = (self.f[1] / self.m) / self.p[0]
        else:
            a = (self.f[1] / self.m) / (self.p[0] * (1 - (1 / ((self.p[1].m/self.m) + 1))))
        b = a
        try:
            a += self.p[1].a[0] * math.cos(self.p[1].a[1] - self.x - 90) / (self.p[0] / ((self.p[1].m/self.m) + 1))
        except:
            a = b
        self.v += a * dt
        self.x += self.v * dt
        if (self.n[1] != None):
            self.n[1].elapse(dt)
    
    def __init__(self, mass, length, previous = None):
        self.m = mass
        #Angular
        self.x = random.random()
        self.v = 0
        self.f_max = mass * g
        #Link
        self.p = [length, previous]
        self.n = [0, None]
        #Cartesian
        self.a = [0,0] #Not relative
        self.c = [0,0]
        self.coords()
        #Forces
        self.f = [0,0] #Normal, Tangential

a = Pendulum()
a.add_node(1,1)
a.add_node(1,1)
a.add_node(1,1)
#a.add_node(1,1)
while (True):
    a.elapse(0.01)
    print(a.start.n[1].a)

    x = [i[0] for i in a.coords()]
    y = [i[1] for i in a.coords()]
    plt.subplots()[0].canvas.draw()
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    plt.plot(x, y, marker="o", markersize=20)
    plt.show()