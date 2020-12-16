from parsy import string, char_from, decimal_digit, seq

MASK_CMD = 'MASK'
MEM_CMD = 'MEM'

mask_line = string('mask = ') >> char_from('X01').many().map(
    lambda mask_chars: (
        MASK_CMD,
        int(''.join(['1' if c == '1' else '0' for c in mask_chars]), 2),  # or mask
        int(''.join(['0' if c == '0' else '1' for c in mask_chars]), 2),  # and mask
    )
)
mem_line = seq(
    string('mem[') >> decimal_digit.many().concat().map(int),
    string('] = ') >> decimal_digit.many().concat().map(int)
).combine(lambda loc, val: (MEM_CMD, loc, val))

code_line = (mem_line | mask_line) << char_from('\n')
code_lines = code_line.many()


OR_MASK = 'OR'
AND_MASK = 'AND'


def execute_pt1(code, memory):
    if not code:
        return memory
    else:
        cmd, x, y = code[0]
        if cmd == MASK_CMD:
            memory[OR_MASK] = x
            memory[AND_MASK] = y
        elif cmd == MEM_CMD:
            val = (memory[OR_MASK] | y) & memory[AND_MASK]
            memory[x] = val
        else:
            raise ValueError(cmd, x, y)
        return execute_pt1(code[1:], memory)


def get_floating_values(float_mask):
    if not float_mask:
        yield 0
    else:
        head = float_mask[-1]
        for val in get_floating_values(float_mask[:-1]):
            if head == 0:
                yield 2 * val
            elif head == 1:
                yield 2 * val
                yield 2 * val + 1


def execute_pt2(code, memory):
    if not code:
        return memory
    else:
        cmd, x, y = code[0]
        if cmd == MASK_CMD:
            memory[OR_MASK] = x
            memory[AND_MASK] = y
        elif cmd == MEM_CMD:
            # AND_MASK is all 1s except for places where mask was exactly 0 (not 1 or X)
            # OR_MASK is all 0s except for places where mask was exactly 1 (not 0 or X)
            # AND_MASK & ~OR_MASK is 1 if AND_MASK is 1 and OR_MASK is 0 -> (0 or X) AND (1 or X)
            float_mask_num = memory[AND_MASK] & ~memory[OR_MASK]
            float_mask = list(map(int, '{:b}'.format(float_mask_num)))
            # set base val to have zeroes where float mask is 1
            base_loc = (x | memory[OR_MASK]) & ~float_mask_num
            for val in get_floating_values(float_mask):
                memory[base_loc | val] = y
        return execute_pt2(code[1:], memory)


def val_sum(memory):
    mem2 = memory.copy()
    del mem2[OR_MASK]
    del mem2[AND_MASK]
    return sum(mem2.values())


def get_solution():
    with open('input/day14_input.txt') as f:
        code = code_lines.parse(''.join(f.readlines()))
        memory = execute_pt1(code, dict())
        print(val_sum(memory))
        memory2 = execute_pt2(code, dict())
        print(val_sum(memory2))
