import os
import numpy
import time
import sys
sys.path.append(r'D:\M_L_Projrct\pythonProject\aiensitan\Config')
import config

class Manual:
    def __init__(self):
        self.blue = [-1, -2, -3, -4, -5, -6]
        self.red = [1, 2, 3, 4, 5, 6]
        self.board = [[0] * 5 for _ in range(5)]  # 初始化真实棋盘
        self.PI = []
        self.CI = []
        self.RCSS = []  # 红色棋子初始设定
        self.BCSS = []

    def createBoard(self, red, blue):  # 新建棋盘，传入红蓝两个参数，就是新棋盘开始时候的布局
        self.RCSS = ['R:']
        self.BCSS = ['B:']
        self.board = [[0] * 5 for _ in range(5)]
        self.board[0][0] = red[0]
        self.RCSS.append('A5-')
        self.RCSS.append(str(int(red[0])))
        self.RCSS.append(';')
        self.board[0][1] = red[1]
        self.RCSS.append('B5-')
        self.RCSS.append(str(int(red[1])))
        self.RCSS.append(';')
        self.board[0][2] = red[2]
        self.RCSS.append('C5-')
        self.RCSS.append(str(int(red[2])))
        self.RCSS.append(';')
        self.board[1][0] = red[3]
        self.RCSS.append('A4-')
        self.RCSS.append(str(int(red[3])))
        self.RCSS.append(';')
        self.board[1][1] = red[4]
        self.RCSS.append('B4-')
        self.RCSS.append(str(int(red[4])))
        self.RCSS.append(';')
        self.board[2][0] = red[5]
        self.RCSS.append('A3-')
        self.RCSS.append(str(int(red[5])))
        self.RCSS.append(';')
        self.board[2][4] = -abs(blue[0])
        self.BCSS.append('E3-')
        self.BCSS.append(str(int(abs(blue[0]))))
        self.BCSS.append(';')
        self.board[3][3] = -abs(blue[1])
        self.BCSS.append('D2-')
        self.BCSS.append(str(int(abs(blue[1]))))
        self.BCSS.append(';')
        self.board[3][4] = -abs(blue[2])
        self.BCSS.append('E2-')
        self.BCSS.append(str(int(abs(blue[2]))))
        self.BCSS.append(';')
        self.board[4][2] = -abs(blue[3])
        self.BCSS.append('C1-')
        self.BCSS.append(str(int(abs(blue[3]))))
        self.BCSS.append(';')
        self.board[4][3] = -abs(blue[4])
        self.BCSS.append('D1-')
        self.BCSS.append(str(int(abs(blue[4]))))
        self.BCSS.append(';')
        self.board[4][4] = -abs(blue[5])
        self.BCSS.append('E1-')
        self.BCSS.append(str(int(abs(blue[5]))))
        self.BCSS.append(';')
        self.PI.append(list(numpy.array(self.board).reshape(25)))

    def appendCI(self, board, chess, rand):
        x = y = -1
        for i in range(5):
            for j in range(5):
                if board[i][j] == chess:
                    x = i
                    y = j
        chess = board[x][y]
        if chess > 0:
            chess = 'R' + str(chess)
        else:
            chess = 'B' + str(-chess)
        x = str(5 - x)
        if y == 0:
            y = 'A'
        elif y == 1:
            y = 'B'
        elif y == 2:
            y = 'C'
        elif y == 3:
            y = 'D'
        elif y == 4:
            y = 'E'
        self.CI.append(':' + str(abs(rand)) + ';(' + chess + ',' + str(y) + str(x) + ')')
        return self.CI

    def Save(self, Winner, CI):

        Team1 = config.get_config('info', 'TEAM1')

        Team2 = config.get_config('info', 'TEAM2')
        Location = config.get_config('info', 'GAME_NAME')
        Name = config.get_config('info', 'GAME_LOCATION')

        dir_name = r'D:\M_L_Projrct\pythonProject\aiensitan\ChessManual'

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        FileName = dir_name + '\\' + 'WTN' + '-' + Team1 + ' ' + 'vs' + ' ' + Team2 + '-'+'Winner is ' + Winner + ' ' + time.strftime(
            "%Y%m%d%H%M",
            time.localtime()) + '.txt'
        Text1 = '#[' + Team1 + '][' + Team2 + '][' + time.strftime("%Y.%m.%d %H:%M",
                                                                   time.localtime()) + ' ' + Location + '][' + Name + '];'
        File = open(FileName, 'w',encoding='utf-8')
        File.write(Text1)
        File.write('\r')
        for RC in self.RCSS:
            File.write(RC)
        File.write('\r')
        for BC in self.BCSS:
            File.write(BC)
        File.write('\r')
        for Step in range(len(CI)):
            File.write(str(Step + 1))
            File.write(CI[Step])
            File.write('\r')
        File.close()



if __name__ == '__main__':
    print(111111111111111)