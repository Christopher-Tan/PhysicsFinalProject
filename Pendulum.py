import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy

#Constants
g = 10
def f(array):
    if (len(array) == 2):
        m1 = array[0][0]
        m2 = array[1][0]
        l1 = array[0][1]
        l2 = array[1][1]
        t1 = array[0][2]
        t2 = array[1][2]
        w1 = array[0][3]
        w2 = array[1][3]
        return [w1, w2, (-g * (2 * m1 + m2) * math.sin(t1) - m2 * g * math.sin(t1 - 2 * t2) - 2 * math.sin(t1 - t2) * m2 * ((w2 ** 2) * l2 + (w1 ** 2) * l1 * math.cos(t1 - t2))) / (l1 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2))), (2 * math.sin(t1 - t2) * ((w1 ** 2) * l1 * (m1 + m2) + g * (m1 + m2) * math.cos(t1) + (w2 ** 2) * l2 * m2 * math.cos(t1 - t2))) / (l2 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2)))]


class Pendulum():
    def __init__(s):
        s.nodes = []        
    def add_node(s):
        s.nodes.append([1, 1, math.pi / 2, 0]) #mass, length, theta, omega
    def remove_node(s):
        s.nodes.pop()
    def elapse(s, dt):
        ms = copy.deepcopy(s.nodes)
        a = f(ms)
        ms = copy.deepcopy(s.nodes)
        ms[0][2] += a[0] * (dt / 2)
        ms[1][2] += a[1] * (dt / 2)
        ms[0][3] += a[2] * (dt / 2)
        ms[1][3] += a[3] * (dt / 2)
        b = f(ms)
        ms = copy.deepcopy(s.nodes)
        ms[0][2] += b[0] * (dt / 2)
        ms[1][2] += b[1] * (dt / 2)
        ms[0][3] += b[2] * (dt / 2)
        ms[1][3] += b[3] * (dt / 2)
        c = f(ms)
        ms = copy.deepcopy(s.nodes)
        ms[0][2] += c[0] * dt
        ms[1][2] += c[1] * dt
        ms[0][3] += c[2] * dt
        ms[1][3] += c[3] * dt
        d = f(ms)
        s.nodes[0][2] += (dt / 6) * (a[0] + 2 * b[0] + 2 * c[0] + d[0])
        s.nodes[1][2] += (dt / 6) * (a[1] + 2 * b[1] + 2 * c[1] + d[1])
        s.nodes[0][3] += (dt / 6) * (a[2] + 2 * b[2] + 2 * c[2] + d[2])
        s.nodes[1][3] += (dt / 6) * (a[3] + 2 * b[3] + 2 * c[3] + d[3])
    def coords(s):
        c = [[0, 0]]
        for i in range(len(s.nodes)):
            x = 0
            y = 0
            for j in range(i+1):
                x += s.nodes[j][1] * math.sin(s.nodes[j][2])
                y -= s.nodes[j][1] * math.cos(s.nodes[j][2])
            c.append([x, y])
        return c

p = [Pendulum() for i in range(2)]
for i in p:
    i.add_node()
    i.add_node()

fig = plt.figure()

def animate(i):
    plt.cla()
    for i in p:
        i.elapse(0.05)
        x = [j[0] for j in i.coords()]
        y = [j[1] for j in i.coords()]
        plt.xlim(-10,10)
        plt.ylim(-10,10)
        plt.plot(x, y, marker="o", markersize=2)

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()