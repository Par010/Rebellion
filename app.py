import random
import math
import numpy as np
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

position = random.sample(range(1, GRID_SIZE), NUMBER_OF_AGENTS)
start = 0
shape = (15, 15)
grid = np.array(range(0, GRID_SIZE))
print(grid.reshape(shape))


class Agent:
    def __init__(self):
        global start
        self.perceived_hardship = random.random()
        self.risk_aversion = random.random()
        self.state = QUIET
        self.position = position[start]
        start += 1

    def __str__(self):
        return f"perceived_hardship: {self.perceived_hardship}, risk_aversion:{self.risk_aversion}, " \
               f"state:{self.state}, position:{self.position}"

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

a1 = Agent()

# print(a1.handle_state())
# print(a1)
