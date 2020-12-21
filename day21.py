def parse_line(line):
    ingredients_str, allergens_str = line.split(' (contains ')
    return set(ingredients_str.split(' ')), set(allergens_str[:-1].split(', '))


def get_candidates(allergen, foods):
    to_intersect = [ingredients for ingredients, allergens in foods if allergen in allergens]
    return to_intersect[0].intersection(*to_intersect[1:])


def get_solution():
    with open('input/day21_input.txt') as f:
        foods = [parse_line(line.rstrip()) for line in f.readlines()]
        all_allergens = {allergen for _, allergens in foods for allergen in allergens}
        candidate_dict = {allergen: get_candidates(allergen, foods) for allergen in all_allergens}
        result = {}
        while len(result) != len(all_allergens):
            for allergen, candidates in list(candidate_dict.items()):
                if allergen in result:
                    continue
                if len(candidates) == 1:
                    print('Assigning {} as {}'.format(next(iter(candidates)), allergen))
                    result[allergen] = next(iter(candidates))
                else:
                    candidate_dict[allergen] = candidate_dict[allergen] - set(result.values())
        allergen_ingredients = set(result.values())
        allergen_free_ingrs = sum([
            len([1 for ingredient in ingredients if ingredient not in allergen_ingredients])
            for ingredients, _ in foods
        ])
        print(allergen_free_ingrs)
        print(sorted(result.items(), key=lambda p: p[1]))
        print(','.join(list(map(lambda p: p[1], sorted(result.items(), key=lambda p: p[0])))))
