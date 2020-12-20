from parsy import string, decimal_digit, seq, char_from

from math import prod

TILE_SIZE = 10

number = decimal_digit.at_least(1).concat().map(int)
tile_header = string('Tile ') >> number << string(':\n')
tile_image_line = char_from('.#').map(lambda v: 1 if v == '#' else 0).times(TILE_SIZE).map(tuple)
tile_image = (tile_image_line << string('\n')).times(TILE_SIZE).map(tuple)

tile_parse = seq(tile_header, tile_image << string('\n')).map(tuple)
tiles_parse = tile_parse.many().map(dict)


def get_nth_col(tile, n):
    return tuple([tile[i][n] for i in range(TILE_SIZE)])


def get_left_edge(tile):
    return get_nth_col(tile, 0)


def get_right_edge(tile):
    return get_nth_col(tile, TILE_SIZE - 1)


def get_edges(tile):
    top = tile[0]
    bot = tile[TILE_SIZE - 1]
    left = tuple([tile[i][0] for i in range(TILE_SIZE)])
    right = get_right_edge(tile)
    return {top, bot, left, right}


def find_edge_matches(edge, tiles):
    return [
        tile for tile in tiles
        if edge in get_edges(tile) or edge[::-1] in get_edges(tile)
    ]


def find_matches(tile_idx, tiles):
    matches = []
    my_edges = get_edges(tiles[tile_idx])
    my_edges.update(set(map(lambda l: l[::-1], my_edges)))
    for idx2, tile in tiles.items():
        if idx2 == tile_idx:
            continue
        other_edges = get_edges(tile)
        if any([my_edge in other_edges for my_edge in my_edges]):
            matches.append(idx2)
    return matches


def rotate_tile_cc(tile):  # counterclockwise
    side_len = len(tile)
    return tuple([tuple([tile[i][side_len - j - 1] for i in range(side_len)]) for j in range(side_len)])


def orient_to_match_left(tile, left_edge):
    rot_tile = tile
    while left_edge != get_left_edge(rot_tile) and left_edge[::-1] != get_left_edge(rot_tile):
        rot_tile = rotate_tile_cc(rot_tile)
    if left_edge[::-1] == get_left_edge(rot_tile):
        rot_tile = rot_tile[::-1]
    return rot_tile


def get_tiles_right_from(tile_col, remaining_tiles):
    next_col = []
    for tile in tile_col:
        right_edge = get_right_edge(tile)
        right_candidates = find_edge_matches(right_edge, remaining_tiles)
        if len(right_candidates) == 1:
            next_col.append(orient_to_match_left(right_candidates[0], right_edge))
            remaining_tiles.remove(right_candidates[0])
        else:
            raise ValueError('Ambiguity!')
    for idx, tilel in enumerate(next_col[:-1]):
        tiler = next_col[idx + 1]
        assert (tilel[TILE_SIZE - 1] == tiler[0])
    return next_col


def orient_corner_upper_left(corner_tile, tiles):
    right_edge = get_right_edge(corner_tile)
    right_candidates = find_edge_matches(right_edge, tiles)
    if len(right_candidates) == 0:
        return orient_corner_upper_left(rotate_tile_cc(corner_tile), tiles)
    else:
        bot_edge = corner_tile[TILE_SIZE - 1]
        bot_candidates = find_edge_matches(bot_edge, tiles)
        if len(bot_candidates) == 0:
            return corner_tile[::-1]
        else:
            return corner_tile


def make_puzzle(corner, remaining_tiles):
    # presume the puzzle is square, and remaining tiles contain all but the corner
    side_len = int((len(remaining_tiles) + 1) ** 0.5)
    ul_corner = orient_corner_upper_left(corner, remaining_tiles)
    prev_col = [ul_corner]
    upper_row = [ul_corner]
    for i in range(side_len - 1):
        next_col = get_tiles_right_from(prev_col, remaining_tiles)
        upper_row += next_col
        prev_col = next_col
    as_left_col = [rotate_tile_cc(tile) for tile in upper_row[::-1]]
    prev_col = as_left_col
    cols = [as_left_col]
    for i in range(side_len - 1):
        next_col = get_tiles_right_from(prev_col, remaining_tiles)
        cols.append(next_col)
        prev_col = next_col
    assert (len(remaining_tiles) == 0)
    return [tuple([cols[j][i] for j in range(side_len)]) for i in range(side_len)]


def check_puzzle(puzzle):
    side_len = len(puzzle)
    for row in puzzle:
        for i in range(side_len - 1):
            assert (get_right_edge(row[i]) == get_left_edge(row[i + 1]))
    for i in range(side_len - 1):
        for j in range(side_len):
            assert (puzzle[i][j][TILE_SIZE - 1] == puzzle[i + 1][j][0])


def drop_tile_edges(puzzle):
    return [
        tuple([
            tile[i][j]
            for tile in tile_row
            for j in range(1, TILE_SIZE - 1)
        ])
        for tile_row in puzzle
        for i in range(1, TILE_SIZE - 1)
    ]


def pretty_print(no_edge_puzzle):
    return '\n'.join([
        ''.join(map(lambda v: '#' if v == 1 else '.', row))
        for row in no_edge_puzzle
    ])


def string_to_pattern(pattern_str):
    return [
        [1 if c == '#' else 0 for c in line]
        for line in pattern_str.split('\n')
    ]


def find_pattern(no_edge_puzzle, pattern):
    pat_h = len(pattern)
    pat_w = len(pattern[0])
    puz_len = len(no_edge_puzzle)
    the_puz = list(map(list, no_edge_puzzle))
    pat_count = 0
    for i in range(puz_len - pat_h + 1):
        for j in range(puz_len - pat_w + 1):
            found_pat = True
            for k in range(pat_h):
                if not found_pat:
                    break
                for m in range(pat_w):
                    if not found_pat:
                        break
                    if pattern[k][m] == 1:
                        found_pat &= the_puz[i + k][j + m] == 1
            if found_pat:
                pat_count += 1
                for k in range(pat_h):
                    for m in range(pat_w):
                        if pattern[k][m] == 1:
                            the_puz[i + k][j + m] = 0
    return pat_count, list(map(tuple, the_puz))


def get_solution_int(tiles, pattern):
    tile_matches = {tile_idx: len(find_matches(tile_idx, tiles)) for tile_idx in tiles}
    corners = [tile_idx for tile_idx, num in tile_matches.items() if num == 2]
    print(len(corners))
    print(prod(corners))
    corner = tiles[corners[0]]
    del tiles[corners[0]]
    puzzle = make_puzzle(corner, set(tiles.values()))
    check_puzzle(puzzle)
    no_edges = drop_tile_edges(puzzle)
    all_orients = [
        no_edges,
        rotate_tile_cc(no_edges),
        rotate_tile_cc(rotate_tile_cc(no_edges)),
        rotate_tile_cc(rotate_tile_cc(rotate_tile_cc(no_edges)))
    ]
    all_orients += [puz[::-1] for puz in all_orients]
    for puz in all_orients:
        # print(pretty_print(puz))
        pat_count, rem_puz = find_pattern(puz, pattern)
        if pat_count > 0:
            print('Found it!')
            print(pat_count)
            print(pretty_print(puz))
            print('\n\n')
            print(pretty_print(rem_puz))
            print(sum(map(sum, rem_puz)))
            break


def get_solution():
    file_name = 'input/day20_input.txt'
    sea_monster = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''
    with open(file_name) as f:
        tiles = tiles_parse.parse(''.join(f.readlines()))
        get_solution_int(tiles, string_to_pattern(sea_monster))
