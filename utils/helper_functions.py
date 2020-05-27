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
