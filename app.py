import random
import math
import numpy as np
from pprint import pprint
from collections import defaultdict
from utils.constants import QUIET, ACTIVE, JAILED
from utils.helper_functions import get_coordinates, get_vision_bounds, get_coordinates_in_bound


# global parameters

states = [QUIET, ACTIVE, JAILED]
GOVERNMENT_LEGITIMACY = random.uniform(0.1, 0.9)
VISION = 4
GRID_SIZE = 15*15
INITIAL_COP_DENSITY = 12
AGENT_DENSITY = 82
MAX_JAIL_TERM = 30
NUMBER_OF_AGENTS = math.floor((GRID_SIZE - 1) * AGENT_DENSITY * 0.01)
NUMBER_OF_COPS = math.floor((GRID_SIZE - 1) * INITIAL_COP_DENSITY * 0.01)
k = random.uniform(0.1, 0.9)
NUMBER_OF_ACTIVE_AGENTS = 6


agent_position = random.sample(range(1, GRID_SIZE+1), NUMBER_OF_AGENTS)

cop_position = []
cops_left = NUMBER_OF_COPS

for emp in range(1, 226):
    if emp not in agent_position and cops_left > 0:
        cop_position.append(emp)
        cops_left -= 1
    else:
        pass

agent_start = 0
cop_start = 0
# shape = (15, 15, 2)
# grid_lst = [[x, 0] for x in range(1, GRID_SIZE+1)]
# grid = np.array(grid_lst)

shape = (15, 15)
grid_lst = [x for x in range(1, GRID_SIZE+1)]
d = {x: 0 for x in grid_lst}
grid = np.array(grid_lst)
agent_count = 1
cop_count = 1
print(grid.reshape(shape))
# print(np.where(grid == 79))


class Agent:
    def __init__(self):
        global agent_start
        global agent_count
        global d
        self.id = "A" + str(agent_count)
        self.perceived_hardship = random.uniform(0.1, 0.9)
        self.risk_aversion = random.uniform(0.1, 0.9)
        self.state = QUIET
        self.__new_state = QUIET
        self.position = agent_position[agent_start]
        self.jail_term = 0
        agent_start += 1
        agent_count += 1
        d[self.position] = self.id

    def __str__(self):
        return f"perceived_hardship: {self.perceived_hardship}, risk_aversion:{self.risk_aversion}, " \
               f"state:{self.state}, position:{self.position}"

    # move -> position -> find vision box -> random empty list -> move -> return # of cops, # of active agents
    # change position in original dict and in the next for loop change the state

    def get_active_agents_and_cops_in_vision(self, vision_position_list):
        active_obj_count = 0
        cops_count = 0
        for pos in vision_position_list:
            if d[pos] == self.position:
                pass
            elif d[pos] == 0:
                pass
            elif d[pos].startswith('A'):
                if obj_dict[d[pos]].state == ACTIVE:
                    active_obj_count += 1
            elif d[pos].startswith('C'):
                cops_count += 1
        return [active_obj_count, cops_count]

    def get_empty_positions(self, vision_position_list):
        available_positions = []
        for pos in vision_position_list:
            if d[pos] == self.position:
                pass
            if d[pos] == 0:
                available_positions.append(pos)
        return available_positions

    def vision_analysis(self):
        # get the coordinates for the current position
        position_in_coordinates = get_coordinates(self.position)
        # get the vision bounds by finding the minimum (x,y) coordinate and maximum (x,y) coordinates of the Vision
        # bound
        vision_bounds = get_vision_bounds(position_in_coordinates[0], position_in_coordinates[1])
        # get the empty positions list, number of active agents, and number of cops in the vision coordinates
        vision_position_list = get_coordinates_in_bound(vision_bounds[0], vision_bounds[1],
                                                                               vision_bounds[2], vision_bounds[3])

        return vision_position_list

    def movement(self):
        vision_position_list = self.vision_analysis()
        available_positions = self.get_empty_positions(vision_position_list)
        if len(available_positions) == 0:
            pass
        else:
            chosen_position_to_jump = available_positions[random.randrange(0, len(available_positions))]
            d[self.position] = 0
            self.position = chosen_position_to_jump
            d[chosen_position_to_jump] = self.id
        return 0

    def grievance(self):
        global GOVERNMENT_LEGITIMACY
        return self.perceived_hardship/GOVERNMENT_LEGITIMACY

    def __estimated_arrest_probability(self, number_of_cops, number_of_active_agents):
        global k
        global NUMBER_OF_COPS
        global NUMBER_OF_ACTIVE_AGENTS
        try:
            estimated_arrest_probability = 1 - math.exp(-k * (math.floor(number_of_cops / number_of_active_agents)))
        except ZeroDivisionError:
            estimated_arrest_probability = 1
        return estimated_arrest_probability

    def net_risk(self):
        vision_position_list = self.vision_analysis()
        active_agents_and_cops_in_vision = self.get_active_agents_and_cops_in_vision(vision_position_list)
        return self.__estimated_arrest_probability(active_agents_and_cops_in_vision[0],
                                                   active_agents_and_cops_in_vision[1]) * self.risk_aversion

    def handle_state(self):
        if self.grievance() > self.net_risk() and self.state == QUIET:
            self.state = ACTIVE


class Cop:
    def __init__(self):
        global cop_count
        global cop_start
        self.id = "C" + str(cop_count)
        self.position = cop_position[cop_start]
        d[self.position] = self.id
        cop_count += 1
        cop_start += 1

    def __str__(self):
        return f"id: {self.id}, position:{self.position}"

    def get_empty_positions(self, vision_position_list):
        available_positions = []
        for pos in vision_position_list:
            if d[pos] == self.position:
                pass
            if d[pos] == 0:
                available_positions.append(pos)
        return available_positions

    def vision_analysis(self):
        # get the coordinates for the current position
        position_in_coordinates = get_coordinates(self.position)
        # get the vision bounds by finding the minimum (x,y) coordinate and maximum (x,y) coordinates of the Vision
        # bound
        vision_bounds = get_vision_bounds(position_in_coordinates[0], position_in_coordinates[1])
        # get the empty positions list, number of active agents, and number of cops in the vision coordinates
        vision_position_list = get_coordinates_in_bound(vision_bounds[0], vision_bounds[1],
                                                                               vision_bounds[2], vision_bounds[3])

        return vision_position_list

    def movement(self):
        vision_position_list = self.vision_analysis()
        available_positions = self.get_empty_positions(vision_position_list)
        if len(available_positions) == 0:
            pass
        else:
            chosen_position_to_jump = available_positions[random.randrange(0, len(available_positions))]
            d[self.position] = 0
            self.position = chosen_position_to_jump
            d[chosen_position_to_jump] = self.id
        return 0


obj_lst = [Agent() for x in range(int(NUMBER_OF_AGENTS))]
cops_lst = [Cop() for x in range(int(NUMBER_OF_COPS))]
obj_dict = {}
for obj in obj_lst:
    obj_dict[obj.id] = obj

cop_dict = {}
for cop in cops_lst:
    cop_dict[cop.id] = cop

# print(obj_lst[0].id)
# print(d)
# obj_lst[0].movement()
# print("-------")
# print(d)
# print(cops_lst[0])
print(d)
print("---")
cops_lst[0].movement()
print(d)

# obj_lst[0].handle_state()
#
# print(obj_lst[0].state)
# print(obj_lst[0].id, obj_lst[0].position)
# print(obj_lst[0].movement())
# print(d)
# print(obj_dict['A1'].position)


# for obj in obj_lst:
#     print(obj)
#
# print(d)
# print(a1)print(grid.reshape(shape))
# print(np.where(grid == 79))
# print("----")
# print(a2)
# print(a1.handle_state())
# print(a1)


# obj = Agent()
# print(obj.get_coordinates(103))
# print(obj.get_vision_bounds(12, 6))
# print(obj.get_coordinates_in_bound(8, 2, 16, 10))

# print(obj.get_position_for_coordinates(0, 14))
# print(d[102])