from parsy import string


floor_tile = string('.').result(0)
empty_seat_tile = string('L').result(1)
tile = floor_tile | empty_seat_tile


def count_adjacent_occupied_pt1(i, j, floor_plan):
    count = 0
    for i2 in range(i - 1, i + 1 + 1):
        if 0 <= i2 < len(floor_plan):
            for j2 in range(j - 1, j + 1 + 1):
                if 0 <= j2 < len(floor_plan[0]) and not (i2 == i and j2 == j):
                    count += 1 if floor_plan[i2][j2] == 2 else 0
    return count


def get_new_val_pt1(i, j, floor_plan):
    if floor_plan[i][j] == 0:  # floor stays floor
        return 0
    else:
        adjacent_occupied = count_adjacent_occupied_pt1(i, j, floor_plan)
        if floor_plan[i][j] == 1 and adjacent_occupied == 0:  # empty seat then becomes taken
            return 2
        elif floor_plan[i][j] == 2 and adjacent_occupied >= 4:  # taken seat becomes unoccupied
            return 1
        else:
            return floor_plan[i][j]


def same_floor_plan(floor_plan1, floor_plan2):
    return all([
        all([
            floor_plan1[i][j] == floor_plan2[i][j]
            for j in range(len(floor_plan1[0]))
        ])
        for i in range(len(floor_plan1))
    ])


def get_new_floor_plan(floor_plan, new_val_func):
    return [
        [
            new_val_func(i, j, floor_plan) for j in range(len(floor_plan[0]))
        ]
        for i in range(len(floor_plan))
    ]


def get_fixpoint(floor_plan, new_val_func):
    new_floor = get_new_floor_plan(floor_plan, new_val_func)
    while not same_floor_plan(floor_plan, new_floor):
        floor_plan = new_floor
        new_floor = get_new_floor_plan(floor_plan, new_val_func)
    return new_floor


def count_occupied(floor_plan):
    return sum([
        1 for i in range(len(floor_plan)) for j in range(len(floor_plan[0]))
        if floor_plan[i][j] == 2
    ])


def get_floor_character(val):
    if val == 0:
        return '.'
    elif val == 1:
        return 'L'
    elif val == 2:
        return '#'


def get_plan_string(floor_plan):
    return '\n'.join(
        ''.join(map(get_floor_character, floor_row))
        for floor_row in floor_plan
    )


DIRS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def count_visible_occupied_pt2(i, j, floor_plan):
    count = 0
    for dir_x, dir_y in DIRS:
        i2, j2 = i + dir_x, j + dir_y
        while (0 <= i2 < len(floor_plan)) \
                and (0 <= j2 < len(floor_plan[0])) \
                and (floor_plan[i2][j2] == 0):
            i2, j2 = i2 + dir_x, j2 + dir_y
        if (0 <= i2 < len(floor_plan)) and (0 <= j2 < len(floor_plan[0])):
            count += 1 if floor_plan[i2][j2] == 2 else 0
    return count


def get_new_val_pt2(i, j, floor_plan):
    if floor_plan[i][j] == 0:  # floor stays floor
        return 0
    else:
        visible_occupied = count_visible_occupied_pt2(i, j, floor_plan)
        if floor_plan[i][j] == 1 and visible_occupied == 0:  # empty seat then becomes taken
            return 2
        elif floor_plan[i][j] == 2 and visible_occupied >= 5:  # taken seat becomes unoccupied
            return 1
        else:
            return floor_plan[i][j]


def get_solution():
    with open('input/day11_input.txt') as f:
        floor_plan = [tile.many().parse(line.rstrip()) for line in f.readlines()]
        print(count_occupied(get_fixpoint(floor_plan, get_new_val_pt1)))
        print(count_occupied(get_fixpoint(floor_plan, get_new_val_pt2)))
