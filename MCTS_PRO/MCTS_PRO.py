import copy
import random
import random_start_chess

def MCTS(Board, dice, player):
    di = {}
    for action in make_all_action(Board, dice, player):
        di.update(win_rate(Board, action, player,50))
    max_key = max(di, key=lambda k: di[k])
    return max_key


def random_choice_action(Board, random_dice, player):
    legal_chess = generate_all_action(Board, random_dice, player)
    all_action = get_legal_move(Board, legal_chess, player)
    try:
        a = random.choice(all_action)
    except:
        print(all_action, Board, random_dice, player)
    return random.choice(all_action)
def win_rate(Board, all_action, P_Player,num):
    dict = {}
    all_action = [f'{all_action}']
    win_sum = 0  # 记录模拟获胜的次数
    for action in all_action:
        Reset_Board = move(copy.deepcopy(Board), action, P_Player)  # 记录这个动作的局面
        STEP = num  # 一个动作模拟的次数
        win_sum = 0  # 记录模拟获胜的次数
        for _ in range(STEP):
            Board = copy.deepcopy(Reset_Board)  # 重置棋盘
            player = -P_Player  # 因为根玩家已经走了这个需要计算胜率的动作了
            while True:
                winner = is_win(Board)
                if winner != 0:
                    if winner == P_Player:
                        win_sum += 1
                    break
                random_dice = random.randint(1, 6)  # 随机模拟骰子数
                random_action = random_choice_action(Board, random_dice, player)
                Board = move(Board, random_action, player)
                player = -player
        # print(action,win_sum)
        win_rate = win_sum / STEP
        dict[f'{action}'] = win_rate

    return dict

def move(situation, pre_move, player):
    if player == 1:
        chess = int(pre_move[0])
    else:
        chess = -int(pre_move[0])
    for i in range(5):
        for j in range(5):
            if situation[i][j] == chess:
                if pre_move[1:] == '上':
                    situation[i][j] = 0
                    situation[i - 1][j] = chess
                elif pre_move[1:] == '下':
                    situation[i][j] = 0
                    situation[i + 1][j] = chess
                elif pre_move[1:] == '左':
                    situation[i][j] = 0
                    situation[i][j - 1] = chess
                elif pre_move[1:] == '右':
                    situation[i][j] = 0
                    situation[i][j + 1] = chess
                elif pre_move[1:] == '右下':
                    situation[i][j] = 0
                    situation[i + 1][j + 1] = chess
                elif pre_move[1:] == '左上':
                    situation[i][j] = 0
                    situation[i - 1][j - 1] = chess
                return situation

def is_win(situation):  # 对于根玩家而言，赢返回1，输返回-1
    if situation[0][0] < 0 or situation[4][4] > 0:
        if situation[0][0] < 0:
            return -1
        else:
            return 1

    red = []
    blue = []
    for i in range(5):
        for j in range(5):
            if situation[i][j] > 0:
                red.append(situation[i][j])
            if situation[i][j] < 0:
                blue.append(situation[i][j])
    if not blue or not red:
        if not red:
            return -1
        else:
            return 1
    return 0


def make_all_action(Board, dice, player):
    legal_chess = generate_all_action(Board, dice, player)
    all_action = get_legal_move(Board, legal_chess, player)
    return all_action

def generate_all_action(situation, dice, player):
    if player == -1:
        dice = -dice
    legal_chess = []
    if any(dice in b for b in situation):
        legal_chess.append(abs(dice))
    else:
        count = 0
        while (dice - count) >= 1 and (dice - count) <= 6:
            if any((dice - count) in b for b in situation):
                legal_chess.append(abs(dice - count))
                break
            count += 1
        count = 0
        while (dice + count) >= 1 and (dice + count) <= 6:
            if any((dice + count) in b for b in situation):
                legal_chess.append(abs(dice + count))
                break
            count += 1
        count = 0
        while (dice - count) >= -6 and (dice - count) <= -1:
            if any((dice - count) in b for b in situation):
                legal_chess.append(abs(dice - count))
                break
            count += 1
        count = 0
        while (dice + count) >= -6 and (dice + count) <= -1:
            if any((dice + count) in b for b in situation):
                legal_chess.append(abs(dice + count))
                break
            count += 1

    return legal_chess


def get_legal_move(situation, legal_chess, player):
    legal_move = []
    for chess in legal_chess.copy():
        if player == -1:
            chess = -chess
        for i in range(5):
            for j in range(5):
                if situation[i][j] == chess:
                    if player == 1:  # 假如目前玩家是红色
                        if i < 4:
                            legal_move.append(str(abs(chess)) + '下')
                        if j < 4:
                            legal_move.append(str(abs(chess)) + '右')
                        if i < 4 and j < 4:
                            legal_move.append(str(abs(chess)) + '右下')
                    if player == -1:  # 假如目前玩家是蓝色
                        if i > 0:
                            legal_move.append(str(abs(chess)) + '上')
                        if j > 0:
                            legal_move.append(str(abs(chess)) + '左')
                        if i > 0 and j > 0:
                            legal_move.append(str(abs(chess)) + '左上')
    return legal_move


def MCTS_Pro(Board, all_action, P_Player):
    dict = {}
    all_action = [f'{all_action}']
    win_sum = 0  # 记录模拟获胜的次数
    for action in all_action:
        Reset_Board = move(copy.deepcopy(Board), action, P_Player)  # 记录这个动作的局面
        STEP = 100  # 一个动作模拟的次数
        win_sum = 0  # 记录模拟获胜的次数
        for _ in range(STEP):
            Board = copy.deepcopy(Reset_Board)  # 重置棋盘
            player = -P_Player  # 因为根玩家已经走了这个需要计算胜率的动作了
            while True:
                winner = is_win(Board)
                if winner != 0:
                    if winner == P_Player:
                        win_sum += 1
                    break
                random_dice = random.randint(1, 6)  # 随机模拟骰子数
                random_action = MCTS(Board, random_dice, player)
                Board = move(Board, random_action, player)
                player = -player
        # print(action,win_sum)
        win_rate = win_sum / STEP
        dict[f'{action}'] = win_rate

    return dict





if __name__ == '__main__':
    import time
    a = time.time()
    Board = [[0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, -1, 0, 0, -5],
             [0, -6, 0, 5, 0],
             [0, 0, 0, 0, -4]]

    dice = 2
    player = -1
    for action in make_all_action(Board, dice, player):
        print(MCTS_Pro(Board, action, player))

    print(time.time() - a)









