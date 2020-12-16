from parsy import string, test_char, decimal_digit, seq

from math import prod


field_tag_parse = test_char(lambda c: c != ':', 'field tag letter').many().concat()
number_parse = decimal_digit.at_least(1).concat().map(int)
range_parse = seq(number_parse << string('-'), number_parse).combine(lambda l, r: range(l, r + 1))

field_parse = seq(
    field_tag_parse << string(': '),
    range_parse << string(' or '),
    range_parse
).combine(lambda name, range1, range2: (name, [range1, range2]))
fields_parse = (field_parse << string('\n')).many().map(dict)

ticket_parse = (number_parse << string(',')).many() + number_parse.map(lambda v: [v])

file_parse = seq(
    fields_parse,
    string('\nyour ticket:\n') >> ticket_parse << string('\n'),
    string('\nnearby tickets:\n') >> (ticket_parse << string('\n')).many()
).map(tuple)


def in_any(num, ranges):
    return any([num in r for r in ranges])


def get_fields_valid_for(allowed_fields, field_dict, val):
    return {field for field in allowed_fields if field in field_dict and in_any(val, field_dict[field])}


def solve_fields(field_dict, allowed_field_dict, tickets, fields_to_assign):
    if fields_to_assign:
        for ticket in tickets:  # finds values that can only be in one field
            for i, val in enumerate(ticket):
                if i not in fields_to_assign:
                    continue
                valid_fields = get_fields_valid_for(allowed_field_dict[i], field_dict, val)
                if len(valid_fields) == 1:
                    the_field = list(valid_fields)[0]
                    print('Assigning {} to {}'.format(the_field, i))
                    del field_dict[the_field]
                    result = solve_fields(field_dict, allowed_field_dict, tickets, fields_to_assign - {i})
                    result[i] = the_field
                    return result
                elif len(valid_fields) < len(allowed_field_dict[i]):
                    allowed_field_dict[i] = valid_fields
                    return solve_fields(field_dict, allowed_field_dict, tickets, fields_to_assign)
        else:
            print('Got stuck! Remaining fields: {}'.format(fields_to_assign))
            return dict()
    else:
        return dict()


def check_valid(idx_field_dict, field_range_dict, ticket):
    return all([
        in_any(val, field_range_dict[idx_field_dict[i]])
        for i, val in enumerate(ticket)
    ])


def get_solution():
    with open('input/day16_input.txt') as f:
        field_dict, my_ticket, tickets = file_parse.parse(''.join(f.readlines()))
        ranges = [r for rs in field_dict.values() for r in rs]
        error_rate = 0
        valid_tickets = []
        for ticket in tickets:
            valid = True
            for val in ticket:
                if not in_any(val, ranges):
                    valid = False
                    error_rate += val
            if valid:
                valid_tickets.append(ticket)
        print(error_rate)
        allowed_field_dict = {i: set(field_dict.keys()) for i in range(len(my_ticket))}
        result_dict = solve_fields(field_dict.copy(), allowed_field_dict, valid_tickets, set(range(len(my_ticket))))
        depart_vals = [my_ticket[i] for i in range(len(my_ticket)) if result_dict[i].startswith('departure')]
        print(prod(depart_vals))
