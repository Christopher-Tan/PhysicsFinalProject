import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

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
        s = self.end
        while (s != None):
            self.start.force()
            s.elapse(dt)
            s = s.p[1]
        self.end.coords()
    def coords(self):
        i = self.start
        c = []
        while (i != None):
            c.append(i.c)
            i = i.n[1]
        return c
    def energy(self):
      e = 0
      s = self.start
      while (s != None):
        e += 0.5 * s.m * (s.v ** 2) + s.m * g * s.c[1]
        s = s.n[1]
      return e
       
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
        try:
            a1 = self.f[1] / self.m / self.p[0]
            self.v += a1 * dt
            self.x += self.v * dt
        except:
            pass
        try:
            a2 = self.f[1] * math.cos(self.n[1].x - self.x) / self.m / self.n[0]
            self.n[1].v -= a2 * dt
            self.n[1].x += self.n[1].v * dt
        except:
            pass

   
    def __init__(self, mass, length, previous = None):
        self.m = mass
        #Angular
        self.x = (random.random() - 0.5)/10
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
a = [Pendulum() for i in range(1)]

for i in a:
    i.add_node(1,1)
    i.add_node(1,1)
    i.add_node(1,1)

fig = plt.figure()

def animate(i):
    plt.cla()
    for i in a:
        i.elapse(0.01)
        x = [j[0] for j in i.coords()]
        y = [j[1] for j in i.coords()]
        plt.xlim(-10,10)
        plt.ylim(-10,10)
        plt.plot(x, y, marker="o", markersize=2)

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()