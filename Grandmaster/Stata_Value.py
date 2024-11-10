class Loc:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y


class Board:
    RED_VALUE = [
        [0, 1, 1, 1, 1],
        [1, 2, 2, 2, 2.5],
        [1, 2, 4, 4, 5],
        [1, 2, 4, 8, 10],
        [1, 2.5, 5, 10, 100]
    ]
    BLUE_VALUE = [
        [100, 10, 5, 2.5, 1],
        [10, 8, 4, 2, 1],
        [5, 4, 4, 2, 1],
        [2.5, 2, 2, 2, 1],
        [1, 1, 1, 1, 0]
    ]

    def __init__(self, arr):
        self.RedState = [6] + [1] * 6
        self.BlueState = [6] + [1] * 6
        self.step = 0
        self.board = [row[:] for row in arr]

    def get_piece_faction(self, piece):
        if piece > 0:
            return 1  # 红方为1
        elif piece < 0:
            return -1  # 蓝方为-1
        else:
            return 0

    def is_legal_loc(self, loc):
        return 0 <= loc.x < 5 and 0 <= loc.y < 5

    def game_state(self):
        red_w = [0] * 7
        blue_w = [0] * 7
        red_value = 0
        blue_value = 0

        for i in range(1, 7):
            if self.RedState[i] == 0:
                continue
            red_w[i] += 1
            for j in range(i - 1, 0, -1):
                if self.RedState[j] == 0:
                    red_w[i] += 1
            for j in range(i + 1, 7):
                if self.RedState[j] == 0:
                    red_w[i] += 1

        for i in range(1, 7):
            if self.BlueState[i] == 0:
                continue
            blue_w[i] -= 1
            for j in range(i - 1, 0, -1):
                if self.BlueState[j] == 0:
                    blue_w[i] -= 1
            for j in range(i + 1, 7):
                if self.BlueState[j] == 0:
                    blue_w[i] -= 1

        for i in range(5):
            for j in range(5):
                piece = self.board[i][j]
                if piece > 0:
                    red_value += red_w[piece] * self.RED_VALUE[i][j]
                elif piece < 0:
                    blue_value += blue_w[-piece] * self.BLUE_VALUE[i][j]

        direction = [(1, 0), (1, 1), (0, 1)]
        for i in range(5):
            for j in range(5):
                max_val = 0
                loc = Loc(i, j)
                f = self.get_piece_faction(self.board[i][j])
                if f > 0:  # 红子
                    for dx, dy in direction:
                        point_temp = Loc(loc.x + f * dx, loc.y + f * dy)
                        if self.is_legal_loc(point_temp) and self.board[point_temp.x][point_temp.y] < 0:
                            value_temp = blue_w[-self.board[point_temp.x][point_temp.y]] * \
                                         self.BLUE_VALUE[point_temp.x][point_temp.y]
                            max_val = min(max_val, value_temp)
                    red_value -= 0.17 * max_val
                elif f < 0:  # 蓝子
                    for dx, dy in direction:
                        point_temp = Loc(loc.x + f * dx, loc.y + f * dy)
                        if self.is_legal_loc(point_temp) and self.board[point_temp.x][point_temp.y] > 0:
                            value_temp = red_w[self.board[point_temp.x][point_temp.y]] * self.RED_VALUE[point_temp.x][
                                point_temp.y]
                            max_val = max(max_val, value_temp)
                    blue_value -= 0.17 * max_val

        return red_value + blue_value

def game_state_value(B):
    b = Board(B)
    return b.game_state()




if __name__ == '__main__':
    B = [[0, 0, -6, 0, 0],
         [0, 2, -2, 0, 0],
         [0, 0, 0, 0, 6],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0]]
    print(game_state_value(B))
















