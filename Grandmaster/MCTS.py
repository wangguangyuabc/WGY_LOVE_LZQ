#蒙特卡洛算法，调用这个函数就进行了一次蒙特卡洛模拟
#模拟的本质还是模拟的越准确越好，蒙特卡洛模拟都是随机走子的，为了提高模拟的准确度，我引用神经网络
#估计走子方向获胜的概率，根据概率来确定模拟过程中走子的方向。

import random
import numpy as np
import copy
import Net
from VEGAME import Game

def MCTS(board, position, direction, Game, STEPS, STEP_COUNTS, Move_By_P):
    WINSUM = 0 # 记录胜利的多少次
    Game.Mboard = board # 定义需要模拟的棋盘
    if board[position[0]][position[1]] > 0:     #判断AI是要走红色棋子，还是蓝色棋子
        APlayer = 1
    elif board[position[0]][position[1]] < 0:
        APlayer = -1
    Game.ResetBoard() # 再次复制棋盘，防止python报错
    Game.Move(position, direction)
    Winner = Game.GetWinner()
    if Winner == APlayer:       
        return 1
    else:
        for _ in range(STEPS):
            Game.ResetBoard()
            Game.Move(position, direction)
            Player = - APlayer                  #现在轮到对方走子
            Step_Count = STEP_COUNTS
            while True:
                Rand = random.randint(1, 6) * Player
                position0, position1 = Game.ChooseChess(Rand)
                if random.randint(0,1) == 0:   # 比较粗略的是该走哪个棋子依旧是随机的，这个可以新建一个小的网络解决
                    Game.Move(position0, GetMove(Game.board, position0, Step_Count, Move_By_P))
                else:
                    Game.Move(position1, GetMove(Game.board, position1, Step_Count, Move_By_P))

                Winner = Game.GetWinner()

                if Winner != 0:
                    if Winner == APlayer:
                        WINSUM += 1
                    break
                
                Player = -Player

                Step_Count -= 1

                if Step_Count < 0:
                    if APlayer == 1:        # WINSUM也可以是小数，这里选择不继续进行模拟，直接返回，返回值为AI对胜率的估值
                        WINSUM += Net.Mark(Game.board)
                    else:
                        WINSUM = 1 - Net.Mark(Game.board) + WINSUM
                    break
        #print(WINSUM / STEPS)
        return WINSUM / STEPS   #模拟轮数默认为1 

def GetMove(board, position, Step_Count, Move_By_P): # Move_By_P参数来控制是否按照神经网络返回的概率来模拟走子
    '''

    :param board: 棋盘
    :param position: 要走的棋子的位置
    :param Step_Count: 现在对局已经是多少步数
    :param Move_By_P: 是否按照神经网络输出的概率来模拟走子
    :return: 返回一个用于模拟的棋子方向
    '''
    if board[position[0]][position[1]] > 0:
        if position[0] == 4:
            Move = 0
        elif position[1] == 4:
            Move = 1
        else:
            if Step_Count >= 0 and Move_By_P:
                MoveList = [[position, 0], [position, 1], [position, 2]]
                Move = np.random.choice([0, 1, 2], p=Net.Get_P(board.copy(), MoveList))
            else:
                Move = np.random.randint(0,3)

    elif board[position[0]][position[1]] < 0:
        if position[0] == 0:
            Move = 0
        elif position[1] == 0:
            Move = 1
        else:
            if Step_Count >= 0 and Move_By_P:
                MoveList = [[position, 0], [position, 1], [position, 2]]
                Move = np.random.choice([0, 1, 2], p=Net.Get_P(board.copy(), MoveList))
            else:
                Move = np.random.randint(0,3)

    return Move

if __name__ == '__main__':
    board = np.array([[-2, 0, -6, 0, 0],
                      [0, 0, 2, 0, 0],
                      [0, 0, 0, 0, 6],
                      [0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0]])
    # [[6, 3, 4, 0, 0], [1, 5, 0, 0, 0], [2, 0, 0, 0, -4], [0, 0, 0, -5, -3], [0, 0, -2, -1, -6]]
    position = (1, 1)
    direction = 3
    STEPS = 1000
    STEP_COUNTS = 4

    win_rate = MCTS(board, position, direction, Game(np.zeros((5, 5))), STEPS, STEP_COUNTS,True)
    print(f"胜率: {win_rate}")






