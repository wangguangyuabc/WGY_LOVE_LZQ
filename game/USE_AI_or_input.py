import sys

sys.path.append(r'D:\M_L_Projrct\pythonProject\aiensitan\Grandmaster')
sys.path.append(r'D:\M_L_Projrct\pythonProject\aiensitan\MCTS_PRO')
from aiensitan.Config import config


def use(Board,player,dice,count):
    if player == 1:
        color = 'red'
    else:
        color = 'blue'
    if config.get_config('game',color) == 'Grandmaster':
        import Grandmaster
        return Grandmaster.Grandmaster(Board, dice, player)
    elif config.get_config('game',color) == 'MCTS_PRO':
        import MCTS_PRO_use
        return MCTS_PRO_use.get_move_MCTSPRO(Board, dice, player,count)
    elif config.get_config('game',color) == 'MCTS_PRO_MAX':
        import MCTS_PRO_use
        return MCTS_PRO_use.get_move_MCTSPROMAX(Board, dice, player)
    elif config.get_config('game',color) == 'people':
        return input('请输入想要走的位置:')



