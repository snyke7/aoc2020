from parsy import string, alt




direction_parse = alt(
    string('sw').result((-1, 1)),
    string('se').result((-1, 0)),
    string('nw').result((1, 0)),
    string('ne').result((1, -1)),
    string('w').result((0, 1)),
    string('e').result((0, -1))
)
ordinal_directions = [(1, 0), (1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
directions_parse = direction_parse.many()
directions_list_parse = (directions_parse << string('\n')).many()


def get_destination(dir_list):
    return sum(map(lambda pr: pr[0], dir_list)), sum(map(lambda pr: pr[1], dir_list))


def get_flipped_tiles(dir_list):
    flipped = set()
    for dest in map(get_destination, dir_list):
        if dest not in flipped:
            flipped.add(dest)
        else:
            flipped.remove(dest)
    return flipped


def get_neighbour_tiles(tile_set):
    return {(tx + dx, ty + dy) for tx, ty in tile_set for dx, dy in ordinal_directions}


def count_neighbors(tile, tile_set):
    tx, ty = tile
    return sum((1 for dx, dy in ordinal_directions if (tx + dx, ty + dy) in tile_set))


def next_tile_state(tile_set):
    result = set()
    for neighbor in get_neighbour_tiles(tile_set):
        neighbor_count = count_neighbors(neighbor, tile_set)
        if neighbor in tile_set:
            if neighbor_count == 0 or neighbor_count > 2:
                pass  # black is flipped to white
            else:
                result.add(neighbor)  # tile stays black
        else:
            if neighbor_count == 2:
                result.add(neighbor)  # white is flipped to black
    return result


def get_nth_state(tile_set, n):
    for i in range(n):
        tile_set = next_tile_state(tile_set)
    return tile_set


def get_solution():
    with open('input/day24_input.txt') as f:
        input_str = ''.join(f.readlines())  # input_str_test
        directions_list = directions_list_parse.parse(input_str)
        flipped_tiles = get_flipped_tiles(directions_list)
        print(len(flipped_tiles))
        print(len(get_nth_state(flipped_tiles, 100)))
