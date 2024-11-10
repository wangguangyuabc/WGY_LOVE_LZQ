import copy
import get_dice
import start_chess
import rule
import copy
from print_board import print_board
from USE_AI_or_input import use
from chess_manual import Manual

def COLOR(color):
    if color == 'red':
        return 1
    elif color == 'blue':
        return -1
    else:
        print('输入错误')
        return None


def RE_COLOR(player):
    if player == 1:
        return 'red'
    else:
        return 'blue'
def COUNT(Broad):
    count = 0
    for i in Broad:
        for j in i:
            if j != 0:
                count += 1
    return count

def main():
    print('——————————————————————欢迎来到概率的世界，游戏开始!——————————————————————')
    manual = Manual()
    Broad,red,blue = start_chess.start()
    manual.createBoard(red,blue)
    print_board(Broad)
    player = COLOR(input('请输入先手方(red/blue):'))
    # player = COLOR('red')
    b = copy.deepcopy(Broad)
    while True:
        if rule.is_win(b) != 0:
            print('winner is', RE_COLOR(rule.is_win(b)))
            break
        while True:
            print('=================')
            dice = get_dice.get_dice()
            print('当前骰子数:', dice)
            all_action = rule.make_all_action(b, dice, player)
            print(all_action)
            count = COUNT(b)
            action = use(b, player, dice,count)
            while True:
                if action in all_action:
                    print('要走的方向是:'+action)
                    break
                else:
                    print('输入动作不合法，请重新输入')
                    print('不合法动作是:'+action)
                    action = use(b, player, dice,count)

            if input('是否悔棋(y/n):') == 'n':
                    break
        b = rule.move(b,action,player)
        manual.appendCI(b, int(action[0])*player, dice)
        count += 1
        player = -player
        print('\n')
        print_board(b)
    CI = manual.CI
    manual.Save(RE_COLOR(rule.is_win(b)),CI)


if __name__ == '__main__':

    main()







