import random
from aiensitan.Config import config
def start_red(game_map):
    red = [0,0,0,0,0,0]
    num = 3
    n = 1
    for i in range(len(game_map)):
        for j in range(len(game_map[i][0:num])):
            game_map[i][j] = int(input(f'请输入红方第{n}数字:'))
            red[n - 1] = game_map[i][j]
            n = n+1
        num = num-1
        if num < 0:
            break
    return game_map,red

def start_blue(game_map):
    print('===================')
    blue = [0,0,0,0,0,0]
    num = 3
    n = 1
    for i in range(len(game_map)):
        for j in range(len(game_map[i][0:num])):
            game_map[4-i][4-j] = -int(input(f'请输入蓝方第{n}数字:'))
            blue[n - 1] = game_map[4-i][4-j]
            n = n+1
        num = num - 1
        if num < 0:
            break
    return game_map, blue

def random_start_red(game_map):
    num = 3
    n = 1
    dice_ = [1,2,3,4,5,6]
    red = [0,0,0,0,0,0]
    for i in range(len(game_map)):
        for j in range(len(game_map[i][0:num])):
            game_map[i][j] = random.choice(dice_)
            red[n - 1] = game_map[i][j]
            dice_.remove(game_map[i][j])
            n = n+1
        num = num-1
        if num < 0:
            break
    return game_map,red

def random_start_blue(game_map):
    dice_ = [-1, -2, -3, -4, -5, -6]
    blue = [0,0,0,0,0,0]
    num = 3
    n = 1
    for i in range(len(game_map)):
        for j in range(len(game_map[i][0:num])):
            game_map[4-i][4-j] = random.choice(dice_)
            blue[n - 1] = game_map[4 - i][4 - j]
            dice_.remove(game_map[4-i][4-j])
            n = n+1
        num = num - 1
        if num < 0:
            break
    return game_map,blue

def start():
    model = config.get_config('setting','Board')
    if model == 'input':
        b,red = start_red([[0 for x in range(5)] for y in range(5)])
        borad,blue = start_blue(b)
        return borad,red,blue

    if model == 'random':
        b,red = random_start_red([[0 for x in range(5)] for y in range(5)])
        borad,blue = random_start_blue(b)
        return borad,red,blue





