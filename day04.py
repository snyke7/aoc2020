from parsy import string, seq, alt, test_char, decimal_digit, success, char_from, any_char, eof

fields_oblig = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
field_cid = 'cid'
field_set = fields_oblig | {field_cid}

field = alt(*list(map(string, field_set)))
key_value_pair = seq(
    field << string(':'),
    test_char(lambda c: c not in {' ', '\n'}, 'value char').many().concat(),
).map(tuple)
whitespace = test_char(lambda c: c in {' ', '\n'}, 'whitespace char')

passport = (key_value_pair << whitespace).many().map(dict)

passport_data = (passport << whitespace).many()


def valid_passport_pt1(passport_dict):
    return all((key in passport_dict for key in fields_oblig))


def validate_height(val, unit):
    if unit == 'cm':
        return 150 <= val <= 193
    elif unit == 'in':
        return 59 <= val <= 76
    else:
        return False


validation_failed = any_char.many().result(False)

birth_year = decimal_digit.times(4).concat().map(int).map(lambda v: 1920 <= v <= 2002) | validation_failed
issue_year = decimal_digit.times(4).concat().map(int).map(lambda v: 2010 <= v <= 2020) | validation_failed
expir_year = decimal_digit.times(4).concat().map(int).map(lambda v: 2020 <= v <= 2030) | validation_failed
height = seq(
    decimal_digit.many().concat().map(int),
    string('cm') | string('in'),
).combine(validate_height) | validation_failed
hair_color = (string('#') + char_from('0123456789abcdef').times(6).concat()) | validation_failed
eye_color = alt(*list(map(string, {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'})), validation_failed)
pid = decimal_digit.times(9).concat().map(int) << eof | validation_failed
cid = any_char.many().result(True)
field_parser = {
    'byr': birth_year,
    'iyr': issue_year,
    'eyr': expir_year,
    'hgt': height,
    'hcl': hair_color,
    'ecl': eye_color,
    'pid': pid,
    'cid': cid,
}


def valid_passport_pt2(passport_dict):
    return all((field_parser[key].parse(value) for key, value in passport_dict.items()))


def get_solution():
    with open('input/day04_input.txt') as f:
        file_lines = ''.join(f.readlines())
        passports = passport_data.parse(file_lines)
        passports_present = list(filter(valid_passport_pt1, passports))
        print(len(passports_present))
        passports_valid = list(filter(valid_passport_pt2, passports_present))
        print(len(passports_valid))
