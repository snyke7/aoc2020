from math import gcd


def get_extend_euclid(a, b, s0, s1, t0, t1):
    if b == 0:
        return a, s0, t0
    else:
        q = a // b
        return get_extend_euclid(b, a - q * b, s1, s0 - q * s1, t1, t0 - q * t1)


def get_certified_gcd(a, b):
    return get_extend_euclid(a, b, 1, 0, 0, 1)


def solve_diophantine_homog(a, b):
    d = gcd(a, b)
    return b // d, -a // d   # ax + by = 0 <=> x = b //d * k, y = -a // d * k, k ∈ ℤ


def solve_diophantine(a, b, c):
    c_x, c_y = solve_diophantine_homog(a, b)
    if c == 0:
        return c_x, 0, c_y, 0
    else:
        d, x, y = get_certified_gcd(a, b)
        return c_x, (c // d) * x, c_y, (c // d) * y


def sanitize(input_str):
    return [(int(val), -i) for i, val in enumerate(input_str.split(',')) if val.isnumeric()]


def get_solution_coeffs(a, z_a, b, z_b):
    c_x, o_x, c_y, o_y = solve_diophantine(a, -b, z_b - z_a)
    return b * c_y, b * o_y + z_b


def compute_solution(coeff_list):
    a, z_a = coeff_list[0]
    for b, z_b in coeff_list[1:]:
        a, z_a = get_solution_coeffs(a, z_a, b, z_b)
        a = abs(a)
        z_a = z_a % a
    return a, z_a


def get_optimal(a, z_a):
    pass


def get_solution():
    sol_input = '37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,587,x,x,x,x,x,x,x,x,x,x,' \
                'x,x,x,x,x,x,x,13,19,x,x,x,23,x,x,x,x,x,29,x,733,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17'
    test_input = '1789,37,47,1889'
    coeff_list = sanitize(test_input)
    _, z_a = compute_solution(coeff_list)
    print(z_a)
    print(compute_solution(sanitize(sol_input))[1])
