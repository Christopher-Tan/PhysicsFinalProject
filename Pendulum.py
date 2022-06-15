import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("numpy")
install("matplotlib")
install("scipy")
install("pandas")
while True:
    import math
    import copy
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.widgets import Slider, Button
    from scipy.linalg import lu_solve, lu_factor
    class Pendulum():
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

    #Modes
    #Not Start (Not Help [Not Clicked, Clicked], Help), Start
    help = False
    def fliph(event):
        global help
        if not help:
            ax[0].set_axis_off()
            onrelease(None)
        else:
            ax[0].set_axis_on()
        help = not help
    start = False
    #called once only
    def flips(event):
        global start, help, smass, pendulums, counter, base
        if help:
            fliph(None)
        if len(base.nodes) != 2:
            for i in base.nodes:
                i[1] = 1
        else:
            base.nodes[1][0] = round((2 ** smass.val) * 1000) / 1000
        pendulums = [copy.deepcopy(base) for i in range(spendulum.val)]
        for i in pendulums:
            for j in i.nodes:
                j[2] += ((counter / spendulum.val) - 0.5) / 100
                counter += 1
        start = True
        fig.delaxes(ax[1])
        fig.delaxes(ax[2])
        fig.delaxes(ax[3])
        fig.delaxes(ax[4])
        if len(base.nodes) == 2:
            fig.delaxes(smassax)
            smass = None
        fig.canvas.mpl_disconnect(cid1)
        fig.canvas.mpl_disconnect(cid2)
        fig.canvas.mpl_disconnect(cid3)
    
    #Global Variables
    counter = 0
    closest = None
    pendulums = []
    base = Pendulum()
    #ax[0] = graph, ax[1] = help button, ax[2] = pendulum slider, ax[3] = start button, ax[4] = node slider, ax[5] = speed slider
    
    fig, ax = plt.subplots(6, 1, figsize=(9,7))
    plt.axis('tight')

    ax[0].set_position([0.08,0.1,0.9,0.85])
    ax[1].set_position([0.08,0.9,0.05,0.05])
    ax[2].set_position([0.15,0.03,0.8,0.02])
    ax[3].set_position([0.88,0.9,0.1,0.05])
    ax[4].set_position([0.15,0.01,0.8,0.02])
    ax[5].set_position([0.15,0.05,0.8,0.02])
    smassax = None
    
    #Sliders
    spendulum = Slider(ax[2], "Pendulum(s)", 1, 100, 50, valstep = 1, clip_on = False)
    snode = Slider(ax[4], "Node(s)", 1, 10, 2, valstep = 1, clip_on = False)
    sspeed = Slider(ax[5], "Speed", -2, 2, 0, valstep = 1, clip_on = False)
    smass = None
    #Buttons
    bhelp = Button(ax[1], "?")
    bhelp.on_clicked(fliph)
    bstart = Button(ax[3], "Start")
    bstart.on_clicked(flips)
    #Events
    clicked = False
    def onclick(event):
        if not start and not help:
            if event.inaxes == ax[0]:
                global closest, base, clicked
                coords = base.coords()
                x = event.xdata
                y = event.ydata
                clicked = True
                c = 0, math.inf
                for i in range(1, len(coords)):
                    if ((x - coords[i][0]) ** 2) + ((y - coords[i][1]) ** 2) < c[1]:
                        c = i, ((x - coords[i][0]) ** 2) + ((y - coords[i][1]) ** 2)
                closest = base.nodes[c[0] - 1], coords[c[0] - 1]
    
    def onrelease(event): #flipc
        global closest, clicked
        closest = None
        clicked = False
                

    def onmove(event):
        if clicked and event.inaxes == ax[0]:
            global closest, base
            x = event.xdata
            y = event.ydata
            closest[0][2] = math.pi - math.atan2(x - closest[1][0], y - closest[1][1])
            closest[0][1] = math.sqrt((y - closest[1][1]) ** 2 + (x - closest[1][0]) ** 2)
    cid1 = fig.canvas.mpl_connect('button_press_event', onclick)
    cid2 = fig.canvas.mpl_connect('button_release_event', onrelease)
    cid3 = fig.canvas.mpl_connect('motion_notify_event', onmove)
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
        else:
            M = []
            n = len(array)
            for i in range(n):
                row = []
                for j in range(n):
                    row.append((n - max(i, j)) * math.cos(array[i][2] - array[j][2]))
                M.append(row)
            v = []
            for i in range(n):
                b = 0
                for j in range(n):
                    b -= (n - max(i, j)) * math.sin(array[i][2] - array[j][2]) * array[j][3] ** 2
                b -= g * (n - i) * math.sin(array[i][2])
                v.append(b)
            r = []
            for i in range(n):
                r.append(array[i][3])
            a = lu_solve(lu_factor(M), v, 0)
            for i in range(n):
                r.append(a[i])
            return r
                
    def animate(i):
        global smassax, smass
        sspeed.valtext.set_text("x " + str(2 ** sspeed.val))
        ax[0].cla()
        if not start:
            if snode.val == 2 and smass == None:
                smassax = plt.axes([0.01,0.1,0.02,0.8])
                smassax.set_axis_off()
                smass = Slider(smassax, 'M2:M1', -3, 3, 0, clip_on=False, orientation='vertical')
            elif snode.val == 2 and smass != None:
                smass.valtext.set_text(round((2 ** smass.val) * 1000) / 1000)
            elif smass != None:
                fig.delaxes(smassax)
                smass = None
            
            if (snode.val < len(base.nodes)):
                base.remove_node()
            elif (snode.val > len(base.nodes)):
                base.add_node()
            
            if not help:
                x = [j[0] for j in base.coords()]
                y = [j[1] for j in base.coords()]
                ax[0].set_xlim(-10,10)
                ax[0].set_ylim(-10,10)
                ax[0].plot(x, y, marker="o", markersize=8, color='black')
            else:
                ax[0].set_axis_off()
                ax[0].text(0, 0.9, "To reset the simulation at any time, close the window.")
                ax[0].text(0, 0.8, "The pendulum mass and length are only adjustable for a double pendulum.")
                ax[0].text(0, 0.75, "It might seem that non-double pendulums also have adjustable lengths, but they")
                ax[0].text(0, 0.7, "will be reset to one upon starting the simulation.")
                ax[0].text(0, 0.6, "Click and drag the node to move it.")
                ax[0].text(0, 0.5, "Once starting the simulation, you cannot pause or re-alter anything.")
                ax[0].text(0, 0.4, "Note: the Runge-Kutta 4 method has a relatively minimal error compared to Euler's")
                ax[0].text(0, 0.35, "method, however, over time the error equally builds up and the simulation becomes")
                ax[0].text(0, 0.3, "less accurate: energy might not be conserved, and the pendulum might move incorrectly.")
                ax[0].text(0, 0.25, "The error also increases if you increase the simulation speed.")
        else:
            n = 2 ** sspeed.val
            for i in pendulums:
                i.elapse(0.04 * n)
                x = [j[0] for j in i.coords()]
                y = [j[1] for j in i.coords()]
                ax[0].set_xlim(-10,10)
                ax[0].set_ylim(-10,10)
                ax[0].plot(x, y, marker="o", markersize=8)

    ani = animation.FuncAnimation(fig, animate, interval=10)
    plt.show()
    plt.close()