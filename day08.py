from parsy import string, char_from, decimal_digit, seq

argument = seq(
    char_from('+-').map(lambda c: 1 if c == '+' else -1),
    decimal_digit.many().concat().map(int)
).combine(lambda m, a: m * a)

acc = string('acc ') >> argument.map(lambda a: (a, 1, a))
nop = string('nop ') >> argument.map(lambda a: (0, 1, a))
jmp = string('jmp ') >> argument.map(lambda a: (0, a, a))

eol = string('\n')

instruction = (acc | nop | jmp) << eol


def get_terminates_n_acc_value(instr_list):
    visited = [0] * len(instr_list)
    accumulator = 0
    idx = 0
    while idx < len(instr_list):
        visited[idx] += 1
        if visited[idx] > 1:
            return False, accumulator
        acc_mut, idx_mut, _ = instr_list[idx]
        accumulator += acc_mut
        idx += idx_mut
    return True, accumulator


def get_answer_pt2(instr_list):
    change_idx = 0
    while change_idx < len(instr_list):
        acc_mut, idx_mut, orig = instr_list[change_idx]
        if acc_mut == 0 and orig != 1:
            # acc_mut = 0 means its nop or jmp, if orig = 1 nop is semantically the same as jmp
            new_idx_mut = orig if idx_mut == 1 else 1
            instr_list[change_idx] = acc_mut, new_idx_mut, orig
            terminates, acc_val = get_terminates_n_acc_value(instr_list)
            if terminates:
                return acc_val
            # else reset value to original
            instr_list[change_idx] = acc_mut, idx_mut, orig
        change_idx += 1


def get_solution():
    with open('input/day08_input.txt') as f:
        instr_list = instruction.many().parse(''.join(f.readlines()))
        _, acc_val = get_terminates_n_acc_value(instr_list)
        print(acc_val)
        print(get_answer_pt2(instr_list))
