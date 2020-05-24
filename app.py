import random
import math
import numpy as np
from pprint import pprint
from collections import defaultdict
from utils.constants import QUIET, ACTIVE, JAILED


# global parameters

states = [QUIET, ACTIVE, JAILED]
GOVERNMENT_LEGITIMACY = random.random()
VISION = 7
GRID_SIZE = 15*15
INITIAL_COP_DENSITY = 12
AGENT_DENSITY = 82
MAX_JAIL_TERM = 30
NUMBER_OF_AGENTS = math.floor(GRID_SIZE * AGENT_DENSITY * 0.01)
NUMBER_OF_COPS = math.floor(GRID_SIZE * INITIAL_COP_DENSITY * 0.01)
k = random.random()
NUMBER_OF_ACTIVE_AGENTS = 6


position = random.sample(range(1, GRID_SIZE+1), NUMBER_OF_AGENTS)
start = 0
# shape = (15, 15, 2)
# grid_lst = [[x, 0] for x in range(1, GRID_SIZE+1)]
# grid = np.array(grid_lst)

shape = (15, 15)
grid_lst = [x for x in range(1, GRID_SIZE+1)]
d = {x: 0 for x in grid_lst}
grid = np.array(grid_lst)
agent_count = 1
# print(grid.reshape(shape))
# print(np.where(grid == 79))


class Agent:
    def __init__(self):
        global start
        global agent_count
        global d
        self.id = "A " + str(agent_count)
        self.perceived_hardship = random.random()
        self.risk_aversion = random.random()
        self.state = QUIET
        self.position = position[start]
        self.jail_term = 0
        start += 1
        agent_count += 1
        d[self.position] = self.id

    def __str__(self):
        return f"perceived_hardship: {self.perceived_hardship}, risk_aversion:{self.risk_aversion}, " \
               f"state:{self.state}, position:{self.position}"

    # move -> position -> find vision box -> random empty list -> move -> return # of cops, # of active agents
    # change position in original dict and in the next for loop change the state

    def estimated_arrest_probability(self):
        global k
        global NUMBER_OF_COPS
        global NUMBER_OF_ACTIVE_AGENTS
        return 1 - math.exp(-k*(math.floor(NUMBER_OF_COPS/NUMBER_OF_ACTIVE_AGENTS)))

    def net_risk(self):
        return self.estimated_arrest_probability() * self.risk_aversion

    def grievance(self):
        global GOVERNMENT_LEGITIMACY
        return self.perceived_hardship/GOVERNMENT_LEGITIMACY

    def handle_state(self):
        if self.grievance() > self.estimated_arrest_probability() and self.state == QUIET:
            self.state = ACTIVE


obj_lst = [Agent() for x in range(int(NUMBER_OF_AGENTS))]

for obj in obj_lst:
    print(obj)

print(d)
# print(a1)print(grid.reshape(shape))
# print(np.where(grid == 79))
# print("----")
# print(a2)
# print(a1.handle_state())
# print(a1)

