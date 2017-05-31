import numpy as np
import pandas as pd
import networkx as nx
import matplotlib as mpl
import random
from enum import Enum

# set these values f and p described in the paper:
# PLoS Comput Biol 4(9): e1000190. doi:10.1371/journal.pcbi.1000190

f = 0.5
p = 0.5


# read our file and parse it from Akiva
connectome = pd.read_excel('./OurCElegansNeuronTables.xls',sheet_name="Connectome").as_matrix()
neuronmuscle = pd.read_excel('./OurCElegansNeuronTables.xls',sheet_name="NeuronsToMuscle").as_matrix()
sensory = pd.read_excel('./OurCElegansNeuronTables.xls',sheet_name="Sensory").as_matrix()


# remove neurons not simulated in paper
phar = [ "I1L", "I1R", "I2L", "I2R", "I3", "I4", "I5", "I6", "M2L", "M2R", "M3L", "M3R", "M4", "M5", "MCL", "MCR", "MI", "NSML", "NSMR" ]

rows = []

for c in xrange(0, len(phar)):
  for d in xrange(0, len(connectome)):
    if ((connectome[d,0] == phar[c]) | (connectome[d,1] == phar[c])):
      rows.append(d);

print len(connectome)

connectome = np.delete(connectome, rows, axis=0);

print len(connectome)

A = connectome[:,0]
B = connectome[:,1]


connection_types = connectome[:,2]
num_connections = connectome[:,3]
neurotransmitter_types = connectome[:,4]

muscleneuron = neuronmuscle[:,1]
muscletarget = neuronmuscle[:,2]
muscleconnections = neuronmuscle[:,3]
muscleneurotransmitter = neuronmuscle[:,4]

sensoryneuron = sensory[:,1]



alldata = np.concatenate((A,B))
nodes = np.unique(alldata)

outputs = np.unique(muscleneuron)
inputs = np.unique(sensoryneuron)

alltotal = np.concatenate((A,B,inputs,outputs))
allnodes = np.unique(alltotal)

#print (inputs)
#print (len(inputs))
#print (len(nodes))
#print (len(A))
#print (len(allnodes))

class State(Enum):
  S = 1
  E = 2
  R = 3
  

neighbors = { }
state = { }
newstate = { }
for i in nodes:
  neighbors[i] = []
  state[i] = State.S
  newstate[i] = State.S


for c in xrange(0, len(A)):
  neighbors[B[c]].append(A[c])
  neighbors[A[c]].append(B[c])

#for c in xrange(0, len(nodes)):
#  print len(neighbors[B[c]])


# let's get to work now

random.seed()

for step in xrange(0, 1000):
  for i in nodes:
    if (state[i] == State.S):
      if (random.random() < f):
        newstate[i] = State.E
      else: 
        for n in neighbors[i]:
          if state[n] == State.E:
            newstate[i] = State.E
    elif (state[i] == State.R):
      if (random.random() < p):
        newstate[i] = State.S
    elif (state[i] == State.E):
      newstate[i] = State.R
  for i in nodes:
    state[i] = newstate[i]
    print state[i].name,
  print ""



exit()



# END OF CODE


# old code for diagramming
#drawing_colors = []

# Collects data for node_peers and node_index
#for c in xrange(0,len(nodes)):
#  graph.add_node(nodes[c])

graph = nx.MultiDiGraph()

graph.add_nodes_from(nodes)

neurotransmitters = np.unique(neurotransmitter_types)


for c in xrange(0, len(A)):
#  if neurotransmitter_types[c] == "Glutamate":
    if connection_types[c] != "GapJunction":
      graph.add_edge(A[c],
                 B[c],
                 weight=num_connections[c],
                 key=0,
                 connectiontype=connection_types[c],
                 neurotransmitter=neurotransmitter_types[c])
    else:
      graph.add_edge(A[c],
                 B[c],
                 weight=num_connections[c],
                 key=1,
                 connectiontype=connection_types[c],
                 neurotransmitter=neurotransmitter_types[c])

pos = nx.random_layout(graph)
#print(pos)

nx.draw(graph)
nx.readwrite.write_graphml(graph,'./out.xml',encoding='utf-8',prettyprint=True)

