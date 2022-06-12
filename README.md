# PhysicsFinalProject

## Project description:

This simulation demonstrates the chaotic motion of a double pendulum, given masses and initial positions provided by the user. Double Pendulums operate with the forces of gravity and tension, and each mass rotates in respect to the mass it is attached to (mass one is connected to the fixed point and rotates around that, while mass two is connected to, and thus rotates around, mass one).


## Instructions:

To rearrange the positions of the nodes prior to the simulation, simply click on a node, and click again where you would like it to be placed (the node will follow your mouse). Note that the top node is a fixed point, and will not be movable.

Once you are satisfied with your initial configuration of nodes and masses, you can decide how many pendulums there will be. Each additional pendulum will create a pendulum behind the original configuration with very minuscule adjustments. These adjustments may create dramatic changes in the motion (depending on how the nodes are configured), which is a testament to the chaotic nature of double pendulums. 

After deciding on the number of pendulums, you can begin the simulation to see the motion of the multi-node pendulum(s). Once the simulation begins, you may adjust the simulation speed using the slider along the bottom. In order to reset the simulation, close the window and a fresh window will appear.

On top of the standard double pendulum, we have also included pendulums with up to 10 nodes. The simulation is adjustable and runs in the same way, other than a few key differences.

The key differences:
-Double pendulums have an adjustable mass ratio, the rest do not.
-The lengths of the non-double pendulums are constant. When setting up the initial configuration, they will seem adjustable. However, the lengths will then be scaled back to the initial length with the angles between the nodes left the same. 

While the pendulums for 3 or more nodes don't have as much variability as the double pendulum, it is available if you are interested in seeing what their chaotic motions are like.

## Run:

To run the program simply double click the .py file, or run `python3 Pendulum.py` from the terminal. To exit the entire program, close the terminal window and not the matplotlib window.