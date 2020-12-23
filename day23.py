from collections import deque


def next_state_pt1(state):
    state_n = state.copy()
    the_size = len(state)
    cur_num = state_n[0]
    state_n.rotate(-1)
    nums = [state_n.popleft(), state_n.popleft(), state_n.popleft()]
    dest_num = (cur_num - 2) % the_size + 1
    while dest_num in nums:
        dest_num = (dest_num - 2) % the_size + 1
    state_n.rotate(-state_n.index(dest_num) - 1)
    state_n.appendleft(nums[2])
    state_n.appendleft(nums[1])
    state_n.appendleft(nums[0])
    state_n.rotate(-state_n.index(cur_num) - 1)
    return state_n


def get_nth_state_pt1(state, n):
    for i in range(n):
        state = next_state_pt1(state)
    return state


def get_order(state):
    state_pr = state.copy()
    state_pr.rotate(-state.index(1))
    state_pr.popleft()
    return ''.join(map(str, list(state_pr)))


def get_destination(popped_nums, cur_num, total_nums):
    dest_num = (cur_num - 2) % total_nums + 1
    while dest_num in popped_nums:
        dest_num = (dest_num - 2) % total_nums + 1
    return dest_num


def get_value(state_dict, offset, i):
    if i not in state_dict:
        return i
    else:
        return state_dict[i]


def next_state_pt2(state_dict, cur_num):
    the_size = len(state_dict)
    next1 = state_dict[cur_num]
    next2 = state_dict[next1]
    next3 = state_dict[next2]
    new_cur = state_dict[next3]
    nums = [next1, next2, next3]
    dest_num = (cur_num - 2) % the_size + 1
    while dest_num in nums:
        dest_num = (dest_num - 2) % the_size + 1
    old_next = state_dict[dest_num]
    state_dict[dest_num] = next1
    state_dict[next3] = old_next
    state_dict[cur_num] = new_cur
    return state_dict, new_cur


def get_nth_state_pt2(state, n, cur_num):
    for i in range(n):
        state, cur_num = next_state_pt2(state, cur_num)
    return state


def as_next_dict(the_str):
    return {int(the_str[i]): int(the_str[(i + 1) % len(the_str)]) for i in range(len(the_str))}


def get_order_from_dict(state_dict):
    result = ''
    prev = 1
    while state_dict[prev] != 1:
        result += str(state_dict[prev])
        prev = state_dict[prev]
    return result


def get_solution():
    input_str_real = '459672813'
    input_str_test = '389125467'
    input_str = input_str_real
    start = deque(map(int, input_str))
    print(get_order(get_nth_state_pt1(start, 100)))
    print(get_order_from_dict(get_nth_state_pt2(as_next_dict(input_str), 100, int(input_str[0]))))

    pt2_input = as_next_dict(input_str)
    pt2_input[int(input_str[-1])] = 10
    for i in range(10, 1000000):
        pt2_input[i] = i + 1
    pt2_input[1000000] = int(input_str[0])

    result = get_nth_state_pt2(pt2_input, 10000000, int(input_str[0]))
    next_num = result[1]
    next_num2 = result[next_num]
    print(next_num * next_num2)
