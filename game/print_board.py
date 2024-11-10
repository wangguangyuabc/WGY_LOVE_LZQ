def print_board(selfboard):  # 打印棋盘
    board = ''
    for i in range(5):
        for j in range(5):
            if int(selfboard[i][j]) < 0:
                board += f'\033[44m {abs(selfboard[i][j])} \033[0m'
            elif (selfboard[i][j]) > 0:
                board += f'\033[41m {selfboard[i][j]} \033[0m'
            else:
                board += "\033[47m   \033[0m"
        board += "\n"
    print(board)

if __name__ == '__main__':
    a = [[3, 6, 5, 0, 0], [4, 1, 0, 0, 0], [2, 0, 0, 0, -5], [0, 0, 0, -2, -3], [0, 0, -1, -4, -6]]
    print_board(a)



