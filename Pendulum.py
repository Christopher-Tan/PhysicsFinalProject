while True:
    import math
    import time
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import random
    import copy
    from matplotlib.widgets import Slider, Button

    #Constants
    end = False
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
            f1 = (-l2 * (m2) * (w2 ** 2) * math.sin(t1 - t2) - g * math.sin(t1)) / l1
            f2 = (l1 * (w1 ** 2) * math.sin(t1 - t2) - g * math.sin(t2)) / l2
            a1 = l2 * m2 * math.cos(t1 - t2) / (l1 * (m1 + m2))
            a2 = l1 * math.cos(t1 - t2) / l2
            return [w1, w2, (f1 - a1 * f2) / (1 - a1 * a2), (f2 - a2 * f1) / (1 - a1 * a2)]


    class Pendulum():
        global i
        def __init__(s):
            s.nodes = []
        def add_node(s):
            s.nodes.append([1, 1, 0, 0]) #mass, length, theta, omega
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
    sp = Pendulum()
    def onclick(event):
        if event.inaxes == ax[0]:
            global c, sp
            if (c != None):
                c = None
            else:
                coords = sp.coords()
                x = event.xdata
                y = event.ydata
                closest = 0, math.inf
                for i in range(1,len(coords)):
                    if ((x - coords[i][0]) ** 2) + ((y - coords[i][1]) ** 2) < closest[1]:
                        closest = i, ((x - coords[i][0]) ** 2 + (y - coords[i][1]) ** 2)
                c = sp.nodes[closest[0]-1], coords[closest[0]-1]

        
        #closest node
    def onmove(event):
        global c, sp
        if (c != None):
            x = event.xdata
            y = event.ydata
            c[0][2] = math.pi - math.atan2(x - c[1][0],y - c[1][1])
            c[0][1] = math.sqrt((y - c[1][1]) ** 2 + (x - c[1][0]) ** 2)
            

    def fliph(event):
        global h
        ax[0].xaxis.set_visible(h)
        ax[0].yaxis.set_visible(h)
        h = not h

    counter = 0
    h = False
    s = False
    c = None
    p = []
    fig, ax = plt.subplots(5,1)
    cid1 = fig.canvas.mpl_connect('button_press_event', onclick)
    cid2 = fig.canvas.mpl_connect('motion_notify_event', onmove)
    def flips(event):
        global s,p,h,counter,spendulum,snode,bhelp,end
        s = not s
        h = False
        c = None
        if s:
            p = [copy.deepcopy(sp) for i in range(spendulum.val)]
            for i in p:
                for j in i.nodes:
                    j[2] += ((counter / spendulum.val) - 0.5)/100
                    counter += 1
            fig.delaxes(ax[1])
            fig.delaxes(ax[2])
            fig.delaxes(ax[3])
            fig.delaxes(ax[4])
            fig.canvas.mpl_disconnect(cid1)
            fig.canvas.mpl_disconnect(cid2)
            ax[0].set_axis_on()
            ax[0].xaxis.set_visible(True)
            ax[0].yaxis.set_visible(True)
        else:
            end = True
    #ax[0] = graph, ax[1] = help button, ax[2] = pendulum slider, ax[3] = start button, ax[4] = node slider
    plt.axis('tight')
    ax[0].set_position([0.08,0.1,0.9,0.85])
    ax[1].set_position([0.08,0.90,0.05,0.05])
    ax[2].set_position([0.15,0.03,0.8,0.02])
    ax[3].set_position([0.88,0.90,0.1,0.05])
    ax[4].set_position([0.15,0.01,0.8,0.02])
    bhelp = Button(ax[1], '?')
    bhelp.on_clicked(fliph)
    bstart = Button(ax[3], 'Start')
    bstart.on_clicked(flips)

    spendulum = Slider(ax[2], "Pendulum(s)", 1, 100, 50, valstep=1, clip_on=False)
    snode = Slider(ax[4], "Node(s)", 1, 10, 2, valstep=1, clip_on=False)
    def animate(i):
        global spendulum, p
        if s == False:
            ax[0].cla()
            if (snode.val < len(sp.nodes)):
                sp.remove_node()
            elif (snode.val > len(sp.nodes)):
                sp.add_node()
            if h == False:
                x = [j[0] for j in sp.coords()]
                y = [j[1] for j in sp.coords()]
                ax[0].set_xlim(-10,10)
                ax[0].set_ylim(-10,10)
                ax[0].plot(x, y, marker="o", markersize=8, color="black")
            else:
                ax[0].cla()
                ax[0].set_axis_off()
                ax[0].text(0, 0.9, "To reset the simulation at any time, close the window.")
                ax[0].text(0, 0.85, "The pendulum mass and length are only adjustable for a double pendulum.")
                ax[0].text(0, 0.8, "It might seem that for non-double pendulums you can adjust the length,")
                ax[0].text(0, 0.75, "but it will be reset to one upon starting the simulation.")
                ax[0].text(0, 0.7, "Click the node to pick up and place it.")
                ax[0].text(0, 0.65, "Please do not try to purposely break the simulation by moving the mouse eratically,")
                ax[0].text(0, 0.60, "etc.")
        else:
            ax[0].cla()
            for i in p:
                i.elapse(0.04)
                x = [j[0] for j in i.coords()]
                y = [j[1] for j in i.coords()]
                ax[0].set_xlim(-10,10)
                ax[0].set_ylim(-10,10)
                ax[0].plot(x, y, marker="o", markersize=8)

    ani = animation.FuncAnimation(fig, animate, interval=10)
    
    plt.show()