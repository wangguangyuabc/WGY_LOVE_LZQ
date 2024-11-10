import random


def start_red(game_map):
    num = 3
    n = 1
    dice_ = [1,2,3,4,5,6]
    for i in range(len(game_map)):
        for j in range(len(game_map[i][0:num])):
            game_map[i][j] = random.choice(dice_)
            dice_.remove(game_map[i][j])
            n = n+1
        num = num-1
        if num < 0:
            break
    return game_map

def start_blue(game_map):
    dice_ = [-1, -2, -3, -4, -5, -6]
    num = 3
    n = 1
    for i in range(len(game_map)):
        for j in range(len(game_map[i][0:num])):
            game_map[4-i][4-j] = random.choice(dice_)
            dice_.remove(game_map[4-i][4-j])
            n = n+1
        num = num - 1
        if num < 0:
            break
    return game_map

def random_chess():
    game_map = [[0 for x in range(5)] for y in range(5)]
    game_map = start_blue(game_map)
    game_map = start_red(game_map)
    return game_map

