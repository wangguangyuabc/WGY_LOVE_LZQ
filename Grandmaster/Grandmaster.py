import numpy as np
import os
import MCTS
import math
from tqdm import tqdm
import Net
from VEGAME import Game as VGame
from Stata_Value import game_state_value
import copy


VGame = VGame(np.zeros((5, 5)))  # 初始化虚拟棋盘

class EinStein_Game():
    def __init__(self):
        self.board = np.zeros([5, 5])  # 初始化真实棋盘
        self.Player = 0  # 当前轮到谁走了
        self.UCTSTEPS = 1000  # 蒙特卡洛模拟次数，有几个节点需要模拟，总模拟次数就是这个数的倍数
        self.STEP_COUNT = 4  # 前4步后的蒙特卡罗模拟中，棋子移动方向的概率由神经网络决定    # 为什么让前几步的移动方向按某种概率决定呢？我猜的，可以试试让后几步试试看看效果好不好，具体思路我在MCTS.py里写
        self.P_Threshold = 1 / 4  # 概率阈值需小于1/3  #如果一个走法被神经网络认为概率很低，那就直接不模拟，25%就是这个阈值
        self.Move_By_P = True  # 是否按方向概率模拟，现在是否，就是26行说的这个
        self.Threshold_Mode = True  # 是否根据阈值否决走法，现在是否，就是27行说的这个
        self.Search = False  # 是否搜索，不搜索的话就是神经网络直接走子
        self.Stata_value_Mode = False # 是否进行混合局面评价过滤模式
        self.C = 0.4 # 反探索系数，系数越高，搜索探索的程度越低
        if self.P_Threshold > 1 / 3:  # 这个概率，是个相对概率，如果有三个走法，他们概率相同，那么他们的走子概率都是33.3%，这就是为什么这个阈值不能大于33.3%，其实也可以试试小于33.3%。
            self.P_Threshold = 1 / 3

    def Change_Mode(self):  # 上面介绍两种模式，都有自己的参数（26，27行），这个代码可以让AI根据棋面情况自动调整这两个参数
        if (self.board[:2, :2] < 0).any() or (self.board[-2:, -2:] > 0).any():
            self.STEP_COUNT = 0
            self.P_Threshold = 0
        elif (self.board[:3, :3] < 0).any() or (self.board[-3:, -3:] > 0).any():
            self.STEP_COUNT = 3
            self.P_Threshold = 1 / 4
        else:
            self.STEP_COUNT = 6
            self.P_Threshold = 1 / 4

    def ChooseChess(self, Randnum):
        if Randnum > 0:
            self.Player = 1
            tempboard = np.where(self.board < 0, 0, self.board)
        elif Randnum < 0:
            self.Player = -1
            tempboard = np.where(self.board > 0, 0, self.board)
            Randnum = -Randnum
            tempboard = -tempboard
        tempboard -= Randnum
        if 0 in tempboard:
            return [np.where(tempboard == 0)[0][0], np.where(tempboard == 0)[1][0]], [np.where(tempboard == 0)[0][0],
                                                                                      np.where(tempboard == 0)[1][0]]
        else:
            if (tempboard < 0).all():
                return [np.where(tempboard == tempboard.max())[0][0], np.where(tempboard == tempboard.max())[1][0]], [
                    np.where(tempboard == tempboard.max())[0][0], np.where(tempboard == tempboard.max())[1][0]]
            elif (np.where(tempboard == -Randnum, 12, tempboard) > 0).all():
                tempboard = np.where(tempboard == -Randnum, 12, tempboard)
                return [np.where(tempboard == tempboard.min())[0][0], np.where(tempboard == tempboard.min())[1][0]], [
                    np.where(tempboard == tempboard.min())[0][0], np.where(tempboard == tempboard.min())[1][0]]
            else:
                min = np.where(tempboard < 0, 12, tempboard)
                max = np.where(tempboard > 0, -12, tempboard)
                return [np.where(min == min.min())[0][0], np.where(min == min.min())[1][0]], [
                    np.where(max == max.max())[0][0], np.where(max == max.max())[1][0]]

    def Move(self, position, direction, rand):  # 移动棋子函数，需要移动的棋子的位置，移动的方向，还有摇出来的随机数
        x = position[0]
        y = position[1]

        if self.board[x][y] > 0:  #
            if direction == 0:  # 移动的方向0横1竖2斜
                self.board[x][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
                y += 1
            elif direction == 1:
                self.board[x + 1][y] = self.board[x][y]
                self.board[x][y] = 0.
                x += 1
            elif direction == 2:
                self.board[x + 1][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
                x += 1
                y += 1
        elif self.board[x][y] < 0:
            if direction == 0:
                self.board[x][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
                y -= 1
            elif direction == 1:
                self.board[x - 1][y] = self.board[x][y]
                self.board[x][y] = 0.
                x -= 1
            elif direction == 2:
                self.board[x - 1][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
                x -= 1
                y -= 1

    def Stata_move(self,board,position, direction):
        x = position[0]
        y = position[1]

        if board[x][y] > 0:  #
            if direction == 0:  # 移动的方向0横1竖2斜
                board[x][y + 1] = board[x][y]
                board[x][y] = 0.
                y += 1
            elif direction == 1:
                board[x + 1][y] = board[x][y]
                board[x][y] = 0.
                x += 1
            elif direction == 2:
                board[x + 1][y + 1] = board[x][y]
                self.board[x][y] = 0.
                x += 1
                y += 1
        elif self.board[x][y] < 0:
            if direction == 0:
                board[x][y - 1] = board[x][y]
                board[x][y] = 0.
                y -= 1
            elif direction == 1:
                board[x - 1][y] = board[x][y]
                board[x][y] = 0.
                x -= 1
            elif direction == 2:
                board[x - 1][y - 1] = board[x][y]
                board[x][y] = 0.
                x -= 1
                y -= 1
        return board

    def GetWinner(self):  # 看看谁获胜了
        if self.board[0][0] < 0 or (self.board <= 0).all():
            Winner = -1
        elif self.board[4][4] > 0 or (self.board >= 0).all():
            Winner = 1
        else:
            Winner = 0

        return Winner


    def UCTbyList(self, MoveList, Step_Count):
        Num = len(MoveList)
        N = [0.] * Num
        UCTValue = [0.] * Num
        WinSum = [0.] * Num
        for _ in tqdm(range(self.UCTSTEPS * Num), ncols=50,colour='blue'):
            board = self.board.copy()  # copy一下要进行模拟的棋盘，python是面向对象的，不按值传递也不按引用传递
            i = np.argmax(UCTValue)
            value = MCTS.MCTS(board, MoveList[i][0], MoveList[i][1], VGame, STEPS=1, STEP_COUNTS=Step_Count,
                              Move_By_P=self.Move_By_P)  # value简单来说1就是获胜，0就是失败，从而重新计算uct值
            WinSum[i] += value
            N[i] += 1
            for i in range(Num):
                UCTValue[i] = self.C * WinSum[i] / (N[i] + 1e-99) + (math.log(np.sum(N)) / (N[i] + 1e-99)) ** 0.5
        if self.Stata_value_Mode:
            index_ = []
            for i in range(len(MoveList)):
                p = MoveList[i][0]
                d = MoveList[i][1]
                b = copy.deepcopy(self.board)
                if game_state_value(self.Stata_move(b, p, d))*self.Player <0:
                    index_.append(i)
            if len(index_)!=0:
                win_ = WinSum.copy()
                n = N.copy()
                for i in index_:
                    win_[i] = 0
                index = np.argmax(np.array(win_) / np.array(n))
            else:
                index = np.argmax(np.array(WinSum) / np.array(N))
        else:
            index = np.argmax(np.array(WinSum) / np.array(N))

        position = MoveList[index][0]
        moveDirection = MoveList[index][1]

        return position, moveDirection  # 返回走子和走子方向

    def GetWay(self, Position):  # 获得走子方向，在一些位置上，棋子只能走一个方向
        if Position[0] == 4 and self.board[Position[0]][Position[1]] > 0:
            way = [0]
        elif Position[1] == 4 and self.board[Position[0]][Position[1]] > 0:
            way = [1]
        elif Position[0] == 0 and self.board[Position[0]][Position[1]] < 0:
            way = [0]
        elif Position[1] == 0 and self.board[Position[0]][Position[1]] < 0:
            way = [1]
        else:
            way = [0, 1, 2]
        return way

    def Eight_Move(self, Position0, Position1):
        self.Position0 = Position0  # 可以移动的两个棋子的位置
        self.Position1 = Position1
        if self.Threshold_Mode:
            self.Change_Mode()
        if Position0 == Position1:  # 如果这两个位置一样，那就是只用考虑一个棋子
            Position = Position0
            way = self.GetWay(Position)  # 获取走子方向
            if len(way) == 1:
                moveDirection = way[0]
            else:
                MoveList = []  # MoveList是UCTbyList的参数，方便UCT代码的产物
                for i in range(len(way)):
                    MoveList.append([Position, way[i]])
                if self.Search:
                    if self.Threshold_Mode:
                        P = Net.Get_P(self.board.copy(), MoveList)
                        P = np.where(P < self.P_Threshold, False, True)

                        MoveList = np.array(MoveList,dtype=object)[P]
                        if len(MoveList) == 1:
                            moveDirection = MoveList[0][1]
                        else:
                            _, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
                    else:

                        MoveList = np.array(MoveList, dtype=object)
                        _, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
                else:
                    moveDirection = np.argmax(Net.Get_P(self.board.copy(), MoveList))

        else:
            way0 = self.GetWay(Position0)
            way1 = self.GetWay(Position1)
            MoveList = []
            for i in range(len(way0)):
                MoveList.append([Position0, way0[i]])
            for i in range(len(way1)):
                MoveList.append([Position1, way1[i]])
            if self.Search:
                if self.Threshold_Mode:
                    P = Net.Get_P(self.board.copy(), MoveList)
                    P = np.where(P < self.P_Threshold / 2, False, True)
                    MoveList = np.array(MoveList, dtype=object)[P]

                    if len(MoveList) == 1:
                        moveDirection = MoveList[0][1]
                    else:
                        Position, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
                else:
                    # print(MoveList)
                    MoveList = np.array(MoveList, dtype=object)
                    Position, moveDirection = self.UCTbyList(MoveList, Step_Count=self.STEP_COUNT)
            else:
                Index = np.argmax(Net.Get_P(self.board.copy(), MoveList))
                # if Index <= 2:
                #     Position = MoveList[0][0]
                #     moveDirection = Index
                # else:
                #     Position = MoveList[3][0]
                #     moveDirection = Index - 3
                Position = MoveList[Index][0]
                moveDirection = MoveList[Index][1]

        return Position, moveDirection


def Grandmaster(Board, dice, player):
    board = np.array(Board)
    rand = player * dice
    Game = EinStein_Game()
    Game.board = board
    chessPosition0, chessPosition1 = Game.ChooseChess(rand)  # 根据随机数得到AI可以走的棋子的位置，可能有一个，或者两个。如果是一个那么这两个Position值就是一样的。
    # tic = time.time()  # 记录AI思考开始的时间
    position, moveDirection = Game.Eight_Move(chessPosition0, chessPosition1)  # AI思考，输入可以走的棋子的位置，输出走的棋子的位置和移动的方向。
    # toc = time.time()  # 记录AI结束思考的时间
    # print('AI思考用时：', toc - tic, 's.')
    i = int(position[0])
    j = int(position[1])
    if Board[i][j] > 0:
        if moveDirection == 0:
            d = '右'
        elif moveDirection == 1:
            d = '下'
        elif moveDirection == 2:
            d = '右下'
        else:
            pass
    else:
        if moveDirection == 0:
            d = '左'
        elif moveDirection == 1:
            d = '上'
        elif moveDirection == 2:
            d = '左上'
        else:
            pass

    result = f'{abs(Board[i][j])}{d}'


    return result


if __name__ == '__main__':

    Board = [[0, 0, 0, 0, 0],
             [6, -1, 0, 4, 0],
             [-2, 0, 0, -6, 0],
             [0, 0, 3, 0, 0],
             [0, 5, 0, -5, 0]]
    player = -1
    dice = 3
    print(Grandmaster(Board, player, dice))


# [[[np.int64(4), np.int64(3)], 0], [[np.int64(4), np.int64(3)], 1], [[np.int64(4), np.int64(3)], 2], [[np.int64(2), np.int64(0)], 1]]




