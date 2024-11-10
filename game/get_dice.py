from aiensitan.Config import config
import random

model = config.get_config('setting','DICE_MODE')

def get_dice(model=model):
    if model == 'random':
        return random.randint(1,6)
    elif model == 'input':
        return int(input('请输入骰子点数:'))




