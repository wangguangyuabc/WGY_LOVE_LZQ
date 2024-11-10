from MCTS_PRO import *

def get_move_MCTSPRO(Board, dice, player,count):
    if count > 6:
        di = {}
        for action in make_all_action(Board, dice, player):
            di.update(win_rate(Board, action, player,3000))
        max_key = max(di, key=lambda k: di[k])
        return max_key

    elif count <= 6:
        di = {}
        for action in make_all_action(Board, dice, player):
            di.update(MCTS_Pro(Board, action, player))
        max_key = max(di, key=lambda k: di[k])
        return max_key

def get_move_MCTSPROMAX(Board, dice, player):
        di = {}
        for action in make_all_action(Board, dice, player):
            di.update(win_rate(Board, action, player,3000))
        max_key = max(di, key=lambda k: di[k])
        return max_key


if __name__ == '__main__':
    Board = [[0, 0, 0, 0, 0],
             [-1, 0, 1, 0, 0],
             [0, 0, 0, 0, -5],
             [0, -6, 0, 5, 0],
             [0, 0, 0, 0, -4]]

    dice = 2
    player = -1
    count = 10
    import time
    a = time.time()
    print(get_move_MCTSPROMAX(Board, dice, player))
    print(time.time() - a)





