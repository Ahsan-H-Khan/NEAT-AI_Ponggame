# NEAT-Pong-Python
Using the NEAT algorithm to train an AI to play pong in Python!

The neat algorithm is set up as the following parameters:
- 40 population size, with fitness of 400 stopping the evolution and using max fitness of one species in the poplation.
- Uses absolute actiavtion function (limits learning capacity but easier to execute and smaller training time), no hidden nodes, and has 3 input ( paddle y , ball y and ball distance) and output nodes ( move up, down or stay still).
- Only has feed forward connection between nodes, with no recurrent connections, means full connectivity at the start to speed up learning process.

Refrences : 
https://neat-python.readthedocs.io/en/latest/neat_overview.html 0.92 documentation
Wikipedia : https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies
Evolving Neural Networks Through Augmenting Topologies (2002) by stanley et. al. 
Courtesy of :TechWithTim

