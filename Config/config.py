import configparser
import os

def get_config(section_name, option_name):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')
    return config.get(section_name, option_name).split('#')[0].strip()

if __name__ == '__main__':
    print(get_config('train', 'TRAIN_TIME'))
