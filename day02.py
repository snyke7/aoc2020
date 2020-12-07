from parsy import decimal_digit, string, letter, seq


def is_valid_part1(*, min_count, max_count, count_letter, password):
    return min_count <= len([c for c in password if c == count_letter]) <= max_count


def is_valid_part2(*, min_count, max_count, count_letter, password):
    return (password[min_count - 1] == count_letter) ^ (password[max_count - 1] == count_letter)


char_count = decimal_digit.at_most(2).concat().map(int)
line_parser = seq(
    min_count=char_count,
    __hyphen=string('-'),
    max_count=char_count,
    __whitespace=string(' '),
    count_letter=letter,
    __colon_space=string(': '),
    password=letter.many()
)

line_parser_part1 = line_parser.combine_dict(is_valid_part1)
line_parser_part2 = line_parser.combine_dict(is_valid_part2)


def get_solution():
    with open('day02_input.txt') as f:
        lines = [line.rstrip() for line in f.readlines()]
        result1 = sum([1 for line in lines if line_parser_part1.parse(line)])
        print(result1)
        result2 = sum([1 for line in lines if line_parser_part2.parse(line)])
        print(result2)

