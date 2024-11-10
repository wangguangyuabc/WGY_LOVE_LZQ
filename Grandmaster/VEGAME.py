import numpy as np
import random

class Game():
    def __init__(self, board):
        self.board = board
        self.Mboard = board.copy()
        
    def ResetBoard(self):
        self.board = self.Mboard.copy()

    def ZeroBoard(self):
        self.board = np.zeros([5,5])

    def Move(self, position, direction):    
        x = position[0]
        y = position[1]
        if self.board[x][y] > 0:
            if direction == 0: # 右
                self.board[x][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 1: # 下
                self.board[x + 1][y] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 2: # 右下
                self.board[x + 1][y + 1] = self.board[x][y]
                self.board[x][y] = 0.
        elif self.board[x][y] < 0:
            if direction == 0: # 左
                self.board[x][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 1: # 上
                self.board[x - 1][y] = self.board[x][y]
                self.board[x][y] = 0.
            elif direction == 2: # 左上
                self.board[x - 1][y - 1] = self.board[x][y]
                self.board[x][y] = 0.
        #print('self.board',self.board)

    def ChooseChess(self, Randnum):
        tempboard = self.board.copy()
        if Randnum > 0:
            tempboard = np.where(tempboard < 0, 0, tempboard)
        elif Randnum < 0:
            tempboard = np.where(tempboard > 0, 0, tempboard)
            Randnum = -Randnum
            tempboard = -tempboard
        tempboard -= Randnum
        #print(tempboard)
        if 0 in tempboard:
            return [np.where(tempboard == 0)[0][0], np.where(tempboard == 0)[1][0]], [np.where(tempboard == 0)[0][0], np.where(tempboard == 0)[1][0]]
        else:
            if (tempboard < 0).all():
                return [np.where(tempboard == tempboard.max())[0][0], np.where(tempboard == tempboard.max())[1][0]], [np.where(tempboard == tempboard.max())[0][0], np.where(tempboard == tempboard.max())[1][0]]
            elif (np.where(tempboard == -Randnum, 100, tempboard)>0).all():
                tempboard = np.where(tempboard == -Randnum, 100, tempboard)
                return [np.where(tempboard == tempboard.min())[0][0], np.where(tempboard == tempboard.min())[1][0]], [np.where(tempboard == tempboard.min())[0][0], np.where(tempboard == tempboard.min())[1][0]]
            else:
                min = np.where(tempboard < 0, 100, tempboard)
                max = np.where(tempboard > 0, -100, tempboard)
                return [np.where(min == min.min())[0][0], np.where(min == min.min())[1][0]], [np.where(max == max.max())[0][0], np.where(max == max.max())[1][0]]
    # Movelist = [,,,]
    def GetWinner(self):
        if self.board[0][0] < 0 or (self.board <= 0).all():
            Winner = -1
        elif self.board[4][4] > 0 or (self.board >= 0).all():
            Winner = 1
        else:
            Winner = 0

        return Winner


if __name__ == '__main__':
    import time
    chessPosition0, chessPosition1 = Game.ChooseChess(rand)  # 根据随机数得到AI可以走的棋子的位置，可能有一个，或者两个。如果是一个那么这两个Position值就是一样的。
    tic = time.time()  # 记录AI思考开始的时间
    position, moveDirection = Game.Eight_Move(chessPosition0, chessPosition1)  # AI思考，输入可以走的棋子的位置，输出走的棋子的位置和移动的方向。
    toc = time.time()  # 记录AI结束思考的时间
    print('AI思考用时：', toc - tic, 's.')










