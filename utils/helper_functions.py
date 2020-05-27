import math
VISION = 4


# get position from coordinates
def get_position_for_coordinates(x, y):
    return y*15+x+1


# get coordinates from position
def get_coordinates(position):
    if position % 15 == 0:
        x = 14
    else:
        x = (position % 15) - 1

    y = int(math.ceil(position/15)) - 1
    return [x, y]


# get vision bound coordinates
def get_vision_bounds(x, y):
    # for minimum coordinates
    xmin = x - VISION
    ymin = y - VISION
    xmax = x + VISION
    ymax = y + VISION
    return [xmin, ymin, xmax, ymax]


# get all the coordinates in the vision
def get_coordinates_in_bound(xmin, ymin, xmax, ymax):
    position_list = []
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            normalised_x = get_circular_coordinates(x)
            normalised_y = get_circular_coordinates(y)
            position_list.append(get_position_for_coordinates(normalised_x, normalised_y))
    return position_list


# get circular coordinates
def get_circular_coordinates( x):
    return (x % 15 + 15) % 15


# def get_active_agents_and_cops_in_vision(vision_position_list, position):
#     active_obj_count = 0
#     cops_count = 0
#     for pos in vision_position_list:
#         if app.d[pos] == position:
#             pass
#         elif app.d[pos] == 0:
#             pass
#         elif app.d[pos].startswith('A'):
#             if app.obj_dict[app.d[pos]].state == app.ACTIVE:
#                 active_obj_count += 1
#         elif app.d[pos].startswith('C'):
#             cops_count += 1
#     return [active_obj_count, cops_count]
#
#
# def get_empty_positions(vision_position_list, position):
#     available_positions = []
#     for pos in vision_position_list:
#         if app.d[pos] == position:
#             pass
#         if app.d[pos] == 0:
#             available_positions.append(pos)
#     return available_positions
#
#
# def vision_analysis(position):
#     # get the coordinates for the current position
#     position_in_coordinates = get_coordinates(position)
#     # get the vision bounds by finding the minimum (x,y) coordinate and maximum (x,y) coordinates of the Vision
#     # bound
#     vision_bounds = get_vision_bounds(position_in_coordinates[0], position_in_coordinates[1])
#     # get the empty positions list, number of active agents, and number of cops in the vision coordinates
#     vision_position_list = get_coordinates_in_bound(vision_bounds[0], vision_bounds[1], vision_bounds[2],
#                                                     vision_bounds[3])
#
#     return vision_position_list
