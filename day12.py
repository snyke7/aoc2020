from parsy import string, decimal_digit

int_val = decimal_digit.many().concat().map(int)
north1 = string('N') >> int_val.map(lambda res: lambda x, y, direction: (x + res, y, direction))
east1 =  string('E') >> int_val.map(lambda res: lambda x, y, direction: (x, y - res, direction))
south1 = string('S') >> int_val.map(lambda res: lambda x, y, direction: (x - res, y, direction))
west1  = string('W') >> int_val.map(lambda res: lambda x, y, direction: (x, y + res, direction))
left1  = string('L') >> int_val.map(lambda res: lambda x, y, direction: (x, y, (direction + res // 90) % 4))
right1 = string('R') >> int_val.map(lambda res: lambda x, y, direction: (x, y, (direction - res // 90) % 4))
forward1 = string('F') >> int_val.map(lambda res: lambda x, y, direction: (
    (x + res, y, direction) if direction == 0 else
    (x, y + res, direction) if direction == 1 else
    (x - res, y, direction) if direction == 2 else
    (x, y - res, direction)
))

command_parser_pt1 = north1 | east1 | south1 | west1 | left1 | right1 | forward1


def rotate_waypoint(degrees, x2, y2):
    if degrees == 0:
        return x2, y2
    else:
        return rotate_waypoint(degrees - 90, -y2, x2)


north2 = string('N') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1, y1, x2 + res, y2))
east2 =  string('E') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1, y1, x2, y2 - res))
south2 = string('S') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1, y1, x2 - res, y2))
west2  = string('W') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1, y1, x2, y2 + res))
left2  = string('L') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1, y1, *rotate_waypoint(res, x2, y2)))
right2 = string('R') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1, y1, *rotate_waypoint(360 - res, x2, y2)))
forward2 = string('F') >> int_val.map(lambda res: lambda x1, y1, x2, y2: (x1 + res * x2, y1 + res * y2, x2, y2))

command_parser_pt2 = north2 | east2 | south2 | west2 | left2 | right2 | forward2


def get_final_pos(command_list, start_pos):
    pos = start_pos
    for command in command_list:
        pos = command(*pos)
    return pos


def get_solution():
    with open('input/day12_input.txt') as f:
        lines = [line.rstrip() for line in f.readlines()]
        commands1 = [command_parser_pt1.parse(line) for line in lines]
        pos = get_final_pos(commands1, (0, 0, 3))
        print(pos)
        x, y, _ = pos
        print(abs(x) + abs(y))

        commands2 = [command_parser_pt2.parse(line) for line in lines]
        pos2 = get_final_pos(commands2, (0, 0, 1, -10))
        print(pos2)
        x, y, _, _ = pos2
        print(abs(x) + abs(y))
