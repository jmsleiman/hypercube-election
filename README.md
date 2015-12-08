# hypercube-election
===Simulation of an election in an n-HyperCube===

==What it is==

A n-hypercube is a cube with n nodes, and of dimension d (where 2^d = n). Most hypercubes are 4-hypercubes or greater (so a 2-cube is a square, a 3-cube is a 3D cube, and a 4-cube is a tesseract).

In distributed systems, the hypercube election is a way for nodes to elect a leader, assuming they are connected in a hypercube pattern. This pattern has some interesting properties that I won't go into here.

The election protocol gets each node to do the following:

1. Message your neighbour on your 0 axis
1.1 Tell them your value, your rank, and challenge them to a duel.
2. If you receive a message on any axis, and you haven't reached the same rank, you hold the message for later.
2.1 If you do match rank, or exceed it, read the message.
2.2 If you've yet to be defeated, it's for you: if the value is better than yours, you become defeated, and the origin of the message is your Queen.
2.3 If you've yet to be defeated, but the value is worse than yours, you can rank up.
2.4 If you've been defeated, forward it to your queen.
3. If a node reaches a rank equal to the dimension of the cube, the election is over, and that cube has won.

In the end, the nodes can all reach the Prime Queen by messaging their queens, and the Prime Queen can send messages out by messaging her Vassals -- however, there are better methods to message down to the Peasants than to use this fact. The election is mostly to discover, organically, who will be the Prime Queen.

In a future update, I might reuse some of this code to provide a way to simulate a message propagation from the Queen to the Peasants, along with other methods pertaining to a hypercube.

==Why Python==

At the time, I figured Python was easy, flexible, and was easy to read. It's also fairly common amongst students, who I was targetting. I think those still stand true, but if I were to re-write it, I would be tempted to develop a system with go that runs goroutines for each of the nodes.

Performance isn't terrible. On an Athlon II X4 620, with 16GB of RAM:

A 3-cube:

real    0m0.031s
user    0m0.024s
sys     0m0.008s

A 13-cube:

real    0m41.362s
user    0m39.292s
sys     0m2.020s

According to the memory_profiler module, a 3-cube uses along the lines of 13MiB of RAM to run the main function, and a 9-cube uses roughly the same amount (the 13-cube profiler never finished...). What actually seems to impact the most is exporting the dot files -- since each dot contains every node and many, many lines, they become quite large (at 13-cube, you can expect to use 300MiB just on the source files!). It leads me to assume memory use could be fairly constant -- or at the very least, not O(n), but closer to O(nlogn). Processor time, on the other hand...

It's of course possible to modify the code to only print the last graph, but there goes some of the value of being able to see it at each clock beat...

==How to use it==

Run the main file:

$ python main.py x high

or

$ python main.py x low

Where x is the dimension of the hypercube to be simulated, and the choice of high/low indicates the direction of the results to present.

The end result is a folder filled with dot files, which can be compiled to show the progress of the election at each "clock tick".

Some notes on the visual output:

	* Defeated nodes are rectangles, live nodes are circles. But just because it's a circle doesn't mean it's a queen.
	* Current messages are listed with dashed arrows. Solid arrows with solid heads represent a communication link.
	* Diamond heads represent a Queen-Vassal (or Queen-Peasant) relationship.
	* I haven't figured out a good way to show the node rank. Right now I just display it in brackets. Colours would be the better option, but I would need to have an algorithmic way to set them (and a well-contrasting colour for the text).

The simulation does make some assumptions:
	* That time is consistent throughout the simulation (ie one second at node 1 is also one second at node 2 -- and when node 1 is processing, all other nodes are frozen)
	* Currently it assigns a random number to each node's edge latency. It also generates the node numbers randomly. However, the method hypercube.setConections() does explain how the values line up, so custom nodes could be coded in.
	* There are currently 104 colours set. Please don't go over 104 dimensions. If you'd like to go over 104 dimensions, please modify the node.toDot() method so that it either has access to a larger colour list (reasonable), or recycles its colour list (bad! won't be able to see anything).
	* All communication links are symmetrical, but the latency is not necessarily symmetrical.

Please enjoy and let me know if there are any issues! This was originally supposed to be a homework assignment, but took much longer to complete than expected. I hope someone out there finds this useful in explaining the hypercube election.

I might also add an export to json option, if it gets requested.
