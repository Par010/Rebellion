import random
import math
import numpy as np
import csv
import os
# from utils.constants import QUIET, ACTIVE, JAILED
import constants

# global parameters

states = [constants.QUIET, constants.ACTIVE, constants.JAILED]
# GOVERNMENT_LEGITIMACY = random.uniform(0.1, 0.9)
GOVERNMENT_LEGITIMACY = 0.99
VISION = 3
GRID_SIZE = 15
GRID_SCOPE = GRID_SIZE*GRID_SIZE
INITIAL_COP_DENSITY = 12
AGENT_DENSITY = 82
MAX_JAIL_TERM = 4
NUMBER_OF_AGENTS = math.floor(GRID_SCOPE * AGENT_DENSITY * 0.01)
NUMBER_OF_COPS = math.floor(GRID_SCOPE * INITIAL_COP_DENSITY * 0.01)
k = random.uniform(0.1, 0.9)
# NUMBER_OF_ACTIVE_AGENTS = 6

# randomly assign positions in the GRID_SCOPE for Agents
initial_agent_positions = random.sample(range(1, GRID_SCOPE+1), NUMBER_OF_AGENTS)

# positions for Cops in the initial world
initial_cop_positions = []

# cops left to be placed in the initial world
cops_left = NUMBER_OF_COPS

for pos in range(1, 226):
    # if position in not taken by an Agent and Cops left is more than 1 in the initial world assign the position to Cop
    if pos not in initial_agent_positions and cops_left > 0:
        initial_cop_positions.append(pos)
        cops_left -= 1
    else:
        pass

# tracking number of positions assigned for Agents in the initial world
agent_start = 0

# tracking number of positions assigned for Cops in the initial world
cop_start = 0


shape = (15, 15)

# grid scope [1, 225]
grid_lst = [x for x in range(1, GRID_SCOPE+1)]

# dictionary depicting the world with the grid scope, key is the position and value is the id of either Agent or Cop
# 0 depicts an empty position
d = {x: 0 for x in grid_lst}

grid = np.array(grid_lst)

# a counter used to create unique ids for Agent
agent_count = 1

# a counter used to create unique ids for Cop
cop_count = 1

print(grid.reshape(shape))


# helper functions


# get position from coordinates

def empty_positions_in_world(dt):
    """function takes a dictionary - current world and returns all the empty postions i.e keys with value 0"""
    empty_positions_list = []
    for dic in dt:
        if dt[dic] == 0:
            empty_positions_list.append(dic)
    return empty_positions_list


def get_coordinates_from_position(x, y):
    """function returns the 2D coordinates in the grid from a position index"""
    return y*15+x+1


# get coordinates from position
def get_coordinates(position):
    """function returns coordinates in 2D from a position index"""
    # get the x coordinate through mod on the GRID_SIZE
    if position % 15 == 0:
        x = 14
    else:
        x = (position % 15) - 1

    # get the y coordinate through division on the GRID_SIZE
    y = int(math.ceil(position/15)) - 1
    return [x, y]


# get vision bound coordinates
def get_vision_bounds(x, y):
    """function returns the min (x,y) coordinates and max (x,y) coordinates of the VISION bound from current (x,y)
    position"""
    xmin = x - VISION
    ymin = y - VISION
    xmax = x + VISION
    ymax = y + VISION
    return [xmin, ymin, xmax, ymax]


# get circular coordinates
def get_circular_coordinates(x):
    """function takes coordinate and return normalised coordinate to fit the round grid scope,
    eg. 2 positions to the left of coordinate (1,1) will be (-1,1) but in the round grid it will be (14,1)"""
    return (x % 15 + 15) % 15


# get all the coordinates in the vision
def get_coordinates_in_bound(xmin, ymin, xmax, ymax):
    """function takes the min(x,y) and max(x,y) coordinates and returns the position of every index within the two
    coordinates"""
    # list of positions in the bound
    position_list = []
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            # get normalised values of x and y coordinates
            normalised_x = get_circular_coordinates(x)
            normalised_y = get_circular_coordinates(y)
            # get the position index from normalised x and y coordinates
            position_list.append(get_coordinates_from_position(normalised_x, normalised_y))
    return position_list


def get_active_agents_and_cops_in_vision(vision_position_list, position):
    """function takes position and vision_position_list and returns the number of active agents and cops in the vision
    bounds of the position entered"""
    active_agent_count = 0
    cops_count = 0
    for pos in vision_position_list:
        # if the position is the position of the object requesting do nothing
        if d[pos] == position:
            pass
        # if the position is empty do nothing
        elif d[pos] == 0:
            pass
        # if the entity present at the position in the world is an Agent and is with the status ACTIVE increment
        # active_agent_count by 1
        elif d[pos].startswith('A'):
            if agent_dict[d[pos]].state == constants.ACTIVE:
                active_agent_count += 1
        # if the entity present is a Cop in the world increment cops_count by 1
        elif d[pos].startswith('C'):
            cops_count += 1
    return [active_agent_count, cops_count]


def get_active_agents_list(vision_position_list, position):
    """function takes position and vision_position_list and returns the number of active agents list in the vision
    bounds of the position entered"""
    active_agent_count = []
    for pos in vision_position_list:
        # if the position is the position of the object requesting do nothing
        if d[pos] == position:
            pass
        # if the position is empty do nothing
        elif d[pos] == 0:
            pass
        # if the entity present at the position in the world is an Agent and is with the status ACTIVE append
        # the position to active_agent_count list
        elif d[pos].startswith('A'):
            if agent_dict[d[pos]].state == constants.ACTIVE:
                active_agent_count.append(pos)
        else:
            pass
    return active_agent_count


def get_empty_positions(vision_position_list, position):
    """function returns empty positions in the vision_position_list"""
    available_positions = []
    for pos in vision_position_list:
        # if the position is the position of the object requesting do nothing
        if d[pos] == position:
            pass
        # if the position is empty append to available_positions
        if d[pos] == 0:
            available_positions.append(pos)
    return available_positions


def vision_analysis(position):
    """function takes position index and returns a list with poistions in the VISION bounds of the position"""
    # get the coordinates for the current position
    position_in_coordinates = get_coordinates(position)
    # get the vision bounds by finding the minimum (x,y) coordinate and maximum (x,y) coordinates of the Vision
    # bound
    vision_bounds = get_vision_bounds(position_in_coordinates[0], position_in_coordinates[1])
    # get the empty positions list, number of active agents, and number of cops in the vision coordinates
    vision_position_list = get_coordinates_in_bound(vision_bounds[0], vision_bounds[1], vision_bounds[2],
                                                    vision_bounds[3])

    return vision_position_list

# end of helper functions


class Agent:
    """Agent is a part of general population in the world who can be either in the QUIET, ACTIVE, or JAILED
    state based on the net_risk and grievance"""

    def __init__(self):
        global agent_start
        global agent_count
        global d
        self.id = "A" + str(agent_count)
        # perceived hardship of the Agent, will not change
        # self.perceived_hardship = random.uniform(0.1, 0.9)
        self.perceived_hardship = 0.01
        # risk aversion of the Agent, will not change
        # self.risk_aversion = random.uniform(0.1, 0.9)
        self.risk_aversion = 1
        # initial state of the Agent
        self.state = constants.QUIET
        # new state of the Agent, initialised as QUIET
        self.__new_state = constants.QUIET
        # position of the Agent in the world
        self.position = initial_agent_positions[agent_start]
        # jail term is initialised as 0
        self.jail_term = 0
        agent_start += 1
        agent_count += 1
        # set the position in the world i.e d to id of the Agent
        d[self.position] = self.id

    def __str__(self):
        return f"perceived_hardship: {self.perceived_hardship}, risk_aversion:{self.risk_aversion}, " \
               f"state:{self.state}, position:{self.position}, jail_term: {self.jail_term}"

    def movement(self):
        """method enables the Agent to potentially move to an empty position within its VISION bounds"""
        global d
        # if the Agent is in the JAILED state do nothing
        if self.state is not constants.JAILED:
            # get list of available positions to move for the Agent within its VISION bounds
            vision_position_list = vision_analysis(position=self.position)
            available_positions = get_empty_positions(vision_position_list, position=self.position)
            # if there is no position available do nothing
            if len(available_positions) == 0:
                pass
            else:
                # choose a position from the available options in the VISION bounds
                chosen_position_to_jump = available_positions[random.randrange(0, len(available_positions))]
                d[self.position] = 0
                # change the Agent object position to new position
                self.position = chosen_position_to_jump
                # set the id of the Agent to the position in the world i.e d
                d[chosen_position_to_jump] = self.id
        else:
            pass
        return 0

    def grievance(self):
        """method calculates the grievance of the Agent object"""
        global GOVERNMENT_LEGITIMACY
        return self.perceived_hardship/GOVERNMENT_LEGITIMACY

    def __estimated_arrest_probability(self, number_of_cops, number_of_active_agents):
        """method returns estimated_arrest_probability of the Agent object"""
        global k
        global NUMBER_OF_COPS
        # formula for estimated_arrest_probability is 1-exp(-k*(number of cops in the VISION bounds/
        # number of active agents in the VISION bounds))
        try:
            estimated_arrest_probability = 1 - math.exp(-k * (math.floor(number_of_cops / number_of_active_agents)))
        except ZeroDivisionError:
            estimated_arrest_probability = 1
        # print(estimated_arrest_probability)
        return estimated_arrest_probability

    def net_risk(self):
        """method returns the net_risk which is given by the formula estimated_arrest_probability * risk_aversion"""
        # get the list of positions in the VISION bounds of the Agent
        vision_position_list = vision_analysis(position=self.position)
        # get the number of cops and active agents in the VISION bounds
        active_agents_and_cops_in_vision = get_active_agents_and_cops_in_vision(vision_position_list,
                                                                                position=self.position)
        # print(active_agents_and_cops_in_vision)
        return self.__estimated_arrest_probability(active_agents_and_cops_in_vision[0],
                                                   active_agents_and_cops_in_vision[1]) * self.risk_aversion

    def update_state(self):
        """method updates the state of an Agent object to the handled state in a given pass. This ensures that the
        other Agent objects update their states based on the state from previous pass, ensuring integrity """
        if self.state is not constants.JAILED:
            if self.__new_state != self.state:
                self.state = self.__new_state

    def handle_state(self):
        """method changes the state of the Agent object if the current state is QUIET and the grievance is
        currently higher than the net_risk."""
        # if state is JAILED do nothing
        if self.state is not constants.JAILED:
            # if grievance is higher than net_risk and state is QUIET set the new_state to ACTIVE
            if self.grievance() > self.net_risk() and self.state == constants.QUIET:
                self.__new_state = constants.ACTIVE
            else:
                # if the state was not changed assign new_state as state
                self.__new_state = self.state

    def handle_jailing(self):
        """method handles jailed agents according to the number of jail_terms they are assigned, eventually assign them
        to a random position in the world after the jail_term is over"""
        # if state is JAILED handle state
        if self.state == constants.JAILED:
            # if the jail_term is > 1 reduce the jail term by 1
            if self.jail_term > 1:
                self.jail_term -= 1
            # if jail_term is equal to 1, add the Agent to an empty position in the world and set the state to QUIET
            elif self.jail_term == 1:
                # find an empty position in the world
                available_world_positions = empty_positions_in_world(d)
                # select an empty position at random
                position_selected = available_world_positions[random.randrange(0, len(available_world_positions))]
                # set the position of the agent to position_selected
                self.position = position_selected
                # set the state of the agent to QUIET
                self.state = constants.QUIET
                # set the jail_term back to 0
                self.jail_term -= 1
                # set the id of the Agent in the position in the world, i.e d
                d[position_selected] = self.id


class Cop:
    """Cop is an authoritarian entity in the world which jails the Agents who are rebelling (ACTIVE)
    against the government."""

    def __init__(self):
        global cop_count
        global cop_start
        self.id = "C" + str(cop_count)
        # set the position of the Cop from the initial_cop_positions
        self.position = initial_cop_positions[cop_start]
        # set the position of the Cop in the world i.e d
        d[self.position] = self.id
        cop_count += 1
        cop_start += 1

    def __str__(self):
        return f"id: {self.id}, position:{self.position}"

    def movement(self):
        """method enables the Cop to potentially move to an empty position within its VISION bounds"""
        global d
        # get list of available positions to move for the Cop within its VISION bounds
        vision_position_list = vision_analysis(position=self.position)
        available_positions = get_empty_positions(vision_position_list, position=self.position)
        # if there is no position available do nothing
        if len(available_positions) == 0:
            pass
        else:
            # choose a position from the available options in the VISION bounds
            chosen_position_to_jump = available_positions[random.randrange(0, len(available_positions))]
            d[self.position] = 0
            # change the Cop object position to new position
            self.position = chosen_position_to_jump
            # set the id of the Cop to the position in the world i.e d
            d[chosen_position_to_jump] = self.id
        return 0

    def arrest(self):
        """method handles arresting an ACTIVE Agent object by the Cop object."""
        global agent_dict
        global d
        # look for positions in the vision on the cop
        vision_position_list = vision_analysis(position=self.position)
        # get the list of active agents in the vision
        active_agents_lst = get_active_agents_list(vision_position_list, position=self.position)
        if len(active_agents_lst) == 0:
            pass
        else:
            agent_to_jail_position = random.randrange(0, len(active_agents_lst))
            # choose an agent in random from the list of active agents
            agent_to_jail = active_agents_lst[agent_to_jail_position]
            # print(agent_to_jail)
            # d[agent_to_jail_position] = 0
            # jail the chosen active agent
            agent_dict[d[agent_to_jail]].state = constants.JAILED
            # give the agent a jail term from 1 to max jail term
            agent_dict[d[agent_to_jail]].jail_term = random.randrange(2, MAX_JAIL_TERM+2)
            # print(agent_dict[d[agent_to_jail]])
            # change agent position to unknown - 0
            agent_dict[d[agent_to_jail]].position = None
            # vacate the position of the jailed agent
            d[agent_to_jail] = 0
            # vacate cop's current position
            d[self.position] = 0
            # change cop's position to the active agent's position
            self.position = agent_to_jail
            # update the cop's position
            d[agent_to_jail] = self.id
        return 0


# populate the world initially

# populate Agents initially
agent_lst = [Agent() for x in range(int(NUMBER_OF_AGENTS))]

# populate Cops initially
cops_lst = [Cop() for x in range(int(NUMBER_OF_COPS))]

# agent_dict is used to maintain Agent object reference
agent_dict = {}
for agent in agent_lst:
    agent_dict[agent.id] = agent

# cop_dict is used to maintain Cop object reference
cop_dict = {}
for cop in cops_lst:
    cop_dict[cop.id] = cop

try:
    os.remove('rebellion.csv')

except:
    pass

boundry = ['-' * 15] * 15

# run a number of passes in the world
for a in range(0, 10):
    # for all agents in the world, enable movement
    for agent in agent_lst:
        agent.movement()

    # for all cops in the world, enable movement
    for cop in cops_lst:
        cop.movement()

    # for all agents in the world, enable handle_state, state is potentially changed but not updated at this point
    for agent in agent_lst:
        agent.handle_state()

    # for all agents in the world, enable update_state, state is updated for all agents altogether
    for agent in agent_lst:
        agent.update_state()

    # for all cops in the world, enable arrest
    for cop in cops_lst:
        cop.arrest()

    # for all agents check
    for agent in agent_lst:
        agent.handle_jailing()

    print(
        '--------------------------------------------------------------------------------------------------------------'
        '----------')
    log_table = []
    for i in range(15):
        log_table.append([])

    # generate log data
    for i in range(15):
        strrr = ''
        for j in range(15):
            id = d[get_coordinates_from_position(i, j)]

            state = ''
            for x in agent_lst:
                if x.id == id:
                    state = x.state
                    break

            str_id = str(id)
            if id == 0:
                str_id = ''

            log_table[i].insert(j, str_id + ' ' + state)

    # print log data
    for row in log_table:
        strrr = ''
        for cell in row:
            space = 7 - len(cell)
            for sp in range(space):
                cell = '' + cell + ' '

            strrr = strrr + cell + '|'
        print(strrr)

        print(
            '----------------------------------------------------------------------------------------------------------'
            '--------------')
    print('')
    print(
        '--------------------------------------------------------------------------------------------------------------'
        '----------')

    with open('rebellion.csv', 'a', newline='') as csvfile:
        result = csv.writer(csvfile, dialect='excel')
        result.writerow(["PASS", a+1])
        result.writerow([])
        result.writerow([])
        result.writerow(boundry)
        result.writerows(log_table)
        result.writerow(boundry)
        result.writerow([])
        result.writerow([])

