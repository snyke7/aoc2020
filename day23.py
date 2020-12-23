from collections import deque


def next_state(state):
    state_n = state.copy()
    cur_num = state_n[0]
    state_n.rotate(-1)
    nums = [state_n.popleft(), state_n.popleft(), state_n.popleft()]
    dest_num = (cur_num - 2) % 9 + 1
    while dest_num not in state_n:
        dest_num = (dest_num - 2) % 9 + 1
    state_n.rotate(-state_n.index(dest_num) - 1)
    state_n.appendleft(nums[2])
    state_n.appendleft(nums[1])
    state_n.appendleft(nums[0])
    state_n.rotate(-state_n.index(cur_num) - 1)
    return state_n


def get_nth_state(state, n):
    for i in range(n):
        state = next_state(state)
    return state


def get_order(state):
    state_pr = state.copy()
    state_pr.rotate(-state.index(1))
    state_pr.popleft()
    return ''.join(map(str, list(state_pr)))


def get_solution():
    start = deque(map(int, '459672813'))
    print(get_order(get_nth_state(start, 100)))
