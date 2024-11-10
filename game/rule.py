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

