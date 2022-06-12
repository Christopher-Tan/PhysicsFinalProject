import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy
from matplotlib.widgets import Button

#Constants
g = 10
n = 50
h = False
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
        f1 = (-l2 * (m2) * (w2 ** 2) * math.sin(t1 - t2) - g * math.sin(t1)) / l1
        f2 = (l1 * (w1 ** 2) * math.sin(t1 - t2) - g * math.sin(t2)) / l2
        a1 = l2 * m2 * math.cos(t1 - t2) / (l1 * (m1 + m2))
        a2 = l1 * math.cos(t1 - t2) / l2
        return [w1, w2, (f1 - a1 * f2) / (1 - a1 * a2), (f2 - a2 * f1) / (1 - a1 * a2)]


class Pendulum():
    def __init__(s):
        s.nodes = []        
    def add_node(s, i):
        s.nodes.append([1, 2, 3 * math.pi / 2 + (i / n - 0.5) / 100, 0]) #mass, length, theta, omega
    def remove_node(s):
        s.nodes.pop()
    def elapse(s, dt):
        cs = copy.deepcopy(s.nodes)
        a = f(cs)
        cs = copy.deepcopy(s.nodes)
        for i in range(len(s.nodes) * 2):
            cs[i % len(s.nodes)][2 + (i // len(s.nodes))] += a[i] * (dt / 2)
        b = f(cs)
        cs = copy.deepcopy(s.nodes)
        for i in range(len(s.nodes) * 2):
            cs[i % len(s.nodes)][2 + (i // len(s.nodes))] += b[i] * (dt / 2)
        c = f(cs)
        cs = copy.deepcopy(s.nodes)
        for i in range(len(s.nodes) * 2):
            cs[i % len(s.nodes)][2 + (i // len(s.nodes))] += c[i] * dt
        d = f(cs)
        for i in range(len(s.nodes) * 2):
            s.nodes[i % len(s.nodes)][2 + (i // len(s.nodes))] += (dt / 6) * (a[i] + 2 * b[i] + 2 * c[i] + d[i])
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

p = [Pendulum() for i in range(n)]
for i in range(n):
    p[i].add_node(i)
    p[i].add_node(i)

fig, ax = plt.subplots(2,1)
plt.axis('tight')
ax[0].set_position([0.1, 0.1, 0.8, 0.8])
ax[1].set_position([0.1,0.85,0.05,0.05])
def animate(i):
    if h == False:
        ax[0].cla()
        for i in p:
            i.elapse(0.04)
            x = [j[0] for j in i.coords()]
            y = [j[1] for j in i.coords()]
            ax[0].set_xlim(-10,10)
            ax[0].set_ylim(-10,10)
            ax[0].plot(x, y, marker="o", markersize=8)
    else:
        ax[0].cla()
        ax[0].set_axis_off()
        ax[0].text(0, 0, "Hi")

def flip(event):
    global h
    ax[0].xaxis.set_visible(h)
    ax[0].yaxis.set_visible(h)
    h = not h

ani = animation.FuncAnimation(fig, animate, interval=10)
bhelp = Button(ax[1], '?')
bhelp.on_clicked(flip)
plt.show()