from collections import deque


def combat_round_pt1(player1: deque, player2: deque):
    left = player1.popleft()
    right = player2.popleft()
    if left > right:
        player1.append(left)
        player1.append(right)
    else:  # right > left
        player2.append(right)
        player2.append(left)


def combat_pt1(player1: deque, player2: deque):
    while not (len(player1) == 0 or len(player2) == 0):
        combat_round_pt1(player1, player2)
    return player1 if len(player2) == 0 else player2


def deque_as_tuple(player: deque):
    result_list = []
    new_deque = player.copy()
    while new_deque:
        result_list.append(new_deque.popleft())
    return tuple(result_list)


def combat_round_pt2(player1: deque, player2: deque):
    left = player1.popleft()
    right = player2.popleft()
    if left <= len(player1) and right <= len(player2):
        sub_player1 = player1.copy()
        while len(sub_player1) > left:
            sub_player1.pop()
        sub_player2 = player2.copy()
        while len(sub_player2) > right:
            sub_player2.pop()
        left_won, _ = combat_pt2(sub_player1, sub_player2)
    else:
        left_won = left > right
    if left_won:
        player1.append(left)
        player1.append(right)
    else:
        player2.append(right)
        player2.append(left)


def combat_pt2(player1: deque, player2: deque):
    played_rounds = set()
    while player1 and player2:
        game_state = deque_as_tuple(player1), deque_as_tuple(player2)
        if game_state in played_rounds:
            return True, player1
        else:
            played_rounds.add(game_state)
        combat_round_pt2(player1, player2)
    player1_won = bool(player1)
    return player1_won, player1 if player1_won else player2


def get_score(player: deque):
    card_list = []
    while player:
        card_list.append(player.popleft())
    print(card_list)
    return sum([(len(card_list) - i) * val for i, val in enumerate(card_list)])


def get_solution():
    with open('input/day22_input.txt') as f:
        player1_input, player2_input = ''.join(f.readlines()).split('\n\n')
        player1_list = list(map(int, player1_input.split('\n')[1:]))
        player2_list = list(map(int, player2_input.split('\n')[1:]))
        player1 = deque(player1_list)
        player2 = deque(player2_list)
        winner = combat_pt1(player1, player2)
        print(get_score(winner))

        player1 = deque(player1_list)
        player2 = deque(player2_list)
        left_won, winner = combat_pt2(player1, player2)
        print(get_score(winner))
