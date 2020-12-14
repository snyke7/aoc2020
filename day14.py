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


def execute(code, memory):
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
        return execute(code[1:], memory)


def val_sum(memory):
    mem2 = memory.copy()
    del mem2[OR_MASK]
    del mem2[AND_MASK]
    return sum(mem2.values())


def get_solution():
    with open('input/day14_input.txt') as f:
        code = code_lines.parse(''.join(f.readlines()))
        memory = execute(code, dict())
        print(val_sum(memory))
