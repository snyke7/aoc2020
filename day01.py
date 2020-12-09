def find_2prod(numbers, total):
    number_sub = [total - number for number in numbers]
    for number in number_sub:
        if number in numbers:
            print(number)
            return number * (total - number)
    print('Could not find product! :(')


def find_3prod(numbers, total):
    for number in numbers:
        result = find_2prod(numbers, total - number)
        if result:
            print(number)
            return number * result


def get_solution():
    with open('input/day01_input.txt') as f:
        numbers = [int(line.rstrip()) for line in f.readlines()]
        print(numbers)
        print(find_2prod(numbers, 2020))
        print(find_3prod(numbers, 2020))
