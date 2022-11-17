from logging import *
import os
from colorama import Fore, Style
from colorama import init as _colorama_init
from .terminal import stty_size
_colorama_init()

__all__ = ['make_logger','logger']

def make_logger(name):
    """
    logger package for user
    Input:
        name: name of the logger
    Output:
        logger object
    """
    logger = getLogger(name)
    basicConfig(filename='logger.log',filemode='w',level=INFO)
    logger.setLevel(1) #getting all logs
    std_handler = StreamHandler()

    # determine some max string lengths
    column_length = stty_size()[1]-13
    log_lvl_length = min(max(int(column_length*0.03), 1), 8)
    s1 = '{}.{}s '.format(log_lvl_length, log_lvl_length)
    column_length -= log_lvl_length
    s5 = '-{}.{}s'.format(column_length, column_length)
    
    fmt_str = Fore.CYAN+'%(asctime)s '+Fore.LIGHTGREEN_EX+'%(levelname)'+s1+\
            Fore.LIGHTWHITE_EX+'%(message)'+s5+Fore.RESET
    formatter = Formatter(fmt_str)
    formatter.default_time_format = "%a %H:%M:%S" # stupid Python 3.8 implementation of Formatter
    std_handler.setFormatter(formatter)

    logger.logger.addHandler(std_handler)

    return logger

logger = make_logger("basic_logger")