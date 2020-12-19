from parsy import string, decimal_digit, seq, char_from, any_char, alt, ParseError

from functools import lru_cache as cache


def tail_from_parts(rule_parts):
    if '|' in rule_parts:
        pipe_idx = rule_parts.index('|')
        return [rule_parts[:pipe_idx], rule_parts[pipe_idx+1:]]
    else:
        return [rule_parts]


number = decimal_digit.at_least(1).concat().map(int)
rule_part = string(' ') >> (number | string('|'))
rule_tail = rule_part.at_least(1).map(tail_from_parts)
rule_exact = string(' "') >> any_char << string('"')

parse_rule_parse = seq(
    number << string(':'),
    rule_exact | rule_tail
).map(tuple)

parse_rules_parse = (parse_rule_parse << string('\n')).many().map(dict)

message_parse = char_from('ab').many().concat()
messages_parse = (message_parse << string('\n')).many()

input_parse = seq(parse_rules_parse << string('\n'), messages_parse).map(tuple)


def to_parser(rule_defs):
    @cache()
    def internal_to_parser(idx):
        rule_def = rule_defs[idx]
        if isinstance(rule_def, str):
            return string(rule_def)
        else:
            return alt(*[
                seq(*list(map(internal_to_parser, to_seq))).map(lambda l: ''.join(l))
                for to_seq in rule_def
            ])

    return internal_to_parser(0), internal_to_parser(31), internal_to_parser(42)


def is_message_valid(message, rule_parser):
    try:
        return rule_parser.parse(message)
    except ParseError:
        return False


def is_message_valid_pt2(message, rule31, rule42):
    for i in range(1, 10):
        for j in range(1, 10):
            try:
                result = seq(rule42.times(i + j).concat(), rule31.times(j).concat()).concat().parse(message)
                return result
            except ParseError:
                pass
    return False


def get_solution():
    with open('input/day19_input.txt') as f:
        rules, messages = input_parse.parse(''.join(f.readlines()))
        rule_parser, rule31, rule42 = to_parser(rules)
        valid_messages1 = [msg for msg in messages if is_message_valid(msg, rule_parser)]
        print(len(valid_messages1))
        valid_messages2 = [msg for msg in messages if is_message_valid_pt2(msg, rule31, rule42)]
        print(len(valid_messages2))
