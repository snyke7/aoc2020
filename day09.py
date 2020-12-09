def is_valid_number(preamble, number):
    for left in preamble:
        if number - left in preamble:
            return True
    return False


def get_invalid_numbers(numbers, preamble_length):
    return [
        num for idx, num in list(enumerate(numbers))[preamble_length:]
        if not is_valid_number(numbers[idx - preamble_length:idx], num)
    ]


def get_answer_pt2(numbers):
    invalid_num = get_invalid_numbers(numbers, 25)[0]
    partial_sums = [sum(numbers[:i + 1]) for i in range(len(numbers) + 1)]
    for idx_u, sum_u in enumerate(partial_sums):
        if sum_u > invalid_num:
            for idx_l, sum_l in enumerate(partial_sums):
                if idx_l >= idx_u - 1:
                    break
                if sum_u - sum_l == invalid_num:
                    contiguous = numbers[(idx_l + 1):(idx_u + 1)]
                    return min(contiguous) + max(contiguous)
                elif sum_u - sum_l < invalid_num:
                    break


def get_solution():
    with open('input/day09_input.txt') as f:
        numbers = [int(line.rstrip()) for line in f.readlines()]
        print(get_invalid_numbers(numbers, 25))
        print(get_answer_pt2(numbers))
