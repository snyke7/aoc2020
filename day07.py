from parsy import string, letter, seq, decimal_digit


bag_name = letter.many().concat() + string(' ') + letter.many().concat()
child_bag = seq(decimal_digit.map(int) << string(' '), bag_name << (string(' bags') | string(' bag'))).map(tuple)
child_bag_separator = string(', ') | string('.')
child_bags = string('no other bags.').result(set()) | (child_bag << child_bag_separator).many().map(set)


bag_rule = seq(
    bag_name << string(' bags contain '),
    child_bags
).map(tuple)

bag_rules = (bag_rule << string('\n')).many().map(dict)


def get_children_only(child_set):
    return {child for amount, child in child_set}


def get_parent_bags(input_children, par_child_dict):
    return {
        parent for parent, children in par_child_dict.items()
        if any((child in get_children_only(children) for child in input_children))
    }


def get_all_parent_bags(input_children, par_child_dict):
    new_bags = input_children.copy()
    all_bags = input_children.copy()
    while new_bags:
        all_bags |= new_bags
        new_bags = get_parent_bags(new_bags, par_child_dict) - all_bags
    return all_bags


def count_child_bags(bag, par_child_dict):
    return sum([
        amount * (count_child_bags(child, par_child_dict) + 1)
        for amount, child in par_child_dict[bag]
    ])


def get_solution():
    with open('day07_input.txt') as f:
        text = ''.join(f.readlines())
        result = bag_rules.parse(text)
        my_bag = 'shiny gold'
        my_bags = {my_bag}
        result_pt1 = get_all_parent_bags(my_bags, result) - my_bags
        print(len(result_pt1))
        print(count_child_bags(my_bag, result))

