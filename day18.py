from parsy import string, decimal_digit, generate, char_from

from math import prod

number = decimal_digit.at_least(1).concat().map(int)
operator = string('*') | string('+')
lparen = string('(')
rparen = string(')')
eol = string('\n')
space = string(' ')


@generate
def calc_num():
    next_val = yield lparen | number
    if next_val == '(':
        # do not return since (5 + 3) * 4  -> after getting 5 + 3, still possible to have a * 4 after
        lnum = yield calc_num
    else:
        lnum = next_val
    space_or_end = yield space | char_from(')\n')  # number is definitely there, but operator may not be there
    if space_or_end in ')\n':
        return [lnum]
    else:
        op = yield operator
        yield space
        rnum = yield calc_num
        return [lnum, op] + rnum


def apply_op(lval, op, rval):
    if op == '+':
        return lval + rval
    elif op == '*':
        return lval * rval
    else:
        raise ValueError('Invalid op: {}'.format(op))


def get_result_pt1(exc_list):
    exc_list_eval = [
        get_result_pt1(v) if isinstance(v, list) else v
        for v in exc_list
    ]
    head_result = apply_op(*exc_list_eval[:3])
    if len(exc_list) == 3:
        return head_result
    else:
        return get_result_pt1([head_result] + exc_list[3:])


def get_result_pt2(exc_list):
    exc_list_eval = [
        get_result_pt2(v) if isinstance(v, list) else v
        for v in exc_list
    ]
    while '+' in exc_list_eval:
        add_idx = exc_list_eval.index('+')
        exc_list_eval = (exc_list_eval[:add_idx - 1] +
                         [exc_list_eval[add_idx - 1] + exc_list_eval[add_idx + 1]] +
                         exc_list_eval[add_idx + 2:])
    nums_only = [v for v in exc_list_eval if isinstance(v, int)]
    return prod(nums_only)


def get_solution():
    with open('input/day18_input.txt') as f:
        exercises = calc_num.many().parse(''.join(f.readlines()))
        print(sum(map(get_result_pt1, exercises)))
        print(sum(map(get_result_pt2, exercises)))
