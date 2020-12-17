def get_neighbor_locs3(loc):
    x, y, z = loc
    return {
        (x + i, y + j, z + k)
        for i in range(-1, 2) for j in range(-1, 2) for k in range(-1, 2)
        if not (i == 0 and j == 0 and k == 0)
    }


def get_neighbor_locs4(loc):
    x, y, z, a = loc
    return {
        (x + i, y + j, z + k, a + m )
        for i in range(-1, 2) for j in range(-1, 2) for k in range(-1, 2) for m in range(-1, 2)
        if not (i == 0 and j == 0 and k == 0 and m == 0)
    }


def get_all_neighbor_locs(pocket_dim, neighbor_fun):
    return {neighbor for loc in pocket_dim for neighbor in neighbor_fun(loc)}


def count_neighbors(pocket_dim, loc, neighbor_fun):
    return sum([1 for neighbor in neighbor_fun(loc) if neighbor in pocket_dim])


def get_next_state(pocket_dim, neighbor_fun):
    return {
        loc for loc in get_all_neighbor_locs(pocket_dim, neighbor_fun)
        if ((loc in pocket_dim and 2 <= count_neighbors(pocket_dim, loc, neighbor_fun) <= 3) or
            (loc not in pocket_dim and count_neighbors(pocket_dim, loc, neighbor_fun) == 3))
    }


def get_nth_state(pocket_dim, n, neighbor_fun):
    i = 0
    while i < n:
        pocket_dim = get_next_state(pocket_dim, neighbor_fun)
        i += 1
    return pocket_dim


def get_input():
    with open('input/day17_input.txt') as f:
        return ''.join(f.readlines())


def get_solution():
    pocket_dim3 = {
        (x, y, 0)
        for x, line in enumerate(get_input().splitlines())
        for y, c in enumerate(line.rstrip())
        if c == '#'
    }
    boot_state = get_nth_state(pocket_dim3, 6, get_neighbor_locs3)
    print(len(boot_state))
    pocket_dim4 = {
        (x, y, 0, 0)
        for x, line in enumerate(get_input().splitlines())
        for y, c in enumerate(line.rstrip())
        if c == '#'
    }
    print(len(get_nth_state(pocket_dim4, 6, get_neighbor_locs4)))
