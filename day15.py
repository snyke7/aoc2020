# def get_next_state(last_num, turn, spoken_turn_dict):
#     new_num =
#     spoken_turn_dict[new_num] = turn
#     print(spoken_turn_dict)
#     return new_num, turn + 1, spoken_turn_dict


def initial_state(start_nums):
    the_dict = {num: (i + 1) for i, num in enumerate(start_nums[:-1])}
    return start_nums[-1], len(start_nums), the_dict


def num_iter(start_nums):
    num, turn, turn_dict = initial_state(start_nums)
    while True:
        if num in turn_dict:
            new_num = turn - turn_dict[num]
        else:
            new_num = 0
        turn_dict[num] = turn
        num = new_num
        turn += 1
        yield turn, num


def get_num_at_turn(start_nums, the_turn):
    for turn, num in num_iter(start_nums):
        if turn == the_turn:
            return num


def get_solution():
    start_nums = [19, 0, 5, 1, 10, 13]
    print(get_num_at_turn(start_nums, 2020))
    print(get_num_at_turn(start_nums, 30000000))
