LARGE_PRIME = 20201227


def calc_power(subject_num, target):
    val = 1
    power = 0
    while val != target:
        val = (val * subject_num) % LARGE_PRIME
        power += 1
    return power


def get_power(subject_num, p):
    result = 1
    for i in range(p):
        result = (result * subject_num) % LARGE_PRIME
    return result


def get_solution():
    pow_card = calc_power(7, 1327981)
    pow_door = calc_power(7, 2822615)
    print(pow_door, pow_card)
    enc_key1 = get_power(2822615, pow_card)
    enc_key2 = get_power(1327981, pow_door)
    print(enc_key2, enc_key1)
