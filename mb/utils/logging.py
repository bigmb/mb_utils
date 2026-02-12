from logging import *
import os
import logging.handlers
from colorama import Fore, Back, Style
from colorama import init as _colorama_init
from .terminal import stty_size
_colorama_init()


LEVEL_COLORS = {
    'DEBUG':    Fore.LIGHTBLACK_EX,
    'INFO':     Fore.GREEN,
    'WARNING':  Fore.YELLOW,
    'ERROR':    Fore.RED,
    'CRITICAL': Fore.WHITE + Back.RED + Style.BRIGHT,
}


class ColoredFormatter(Formatter):
    """Formatter that applies per-level colors to console output."""

    def __init__(self, fmt, datefmt=None):
        super().__init__(fmt, datefmt=datefmt)
        self.default_msec_format = None

    def format(self, record):
        color = LEVEL_COLORS.get(record.levelname, Fore.RESET)
        record.levelcolor = color
        record.reset = Style.RESET_ALL
        return super().format(record)

__all__ = ['make_logger','logger', 'logg']


class LoggerWrapper:
    """
    A wrapper that allows calling log methods without checking if logger is None.
    
    Usage:
        from mb_utils.logging import logg
        
        # With explicit logger:
        logg.info('hello', logger)  # If logger is None, does nothing. If logger exists, logs.
        
        # With default logger (set via set_default):
        logg.set_default(make_logger('myapp'))
        logg.info('hello')  # Uses default logger
        
        # Explicit None overrides default (does nothing):
        logg.info('hello', None)
    """
    
    def __init__(self):
        self._default_logger = None
    
    def set_default(self, logger):
        """Set a default logger to use when none is provided."""
        self._default_logger = logger
    
    def _log(self, level, msg, logger=..., *args, **kwargs):
        if logger is ...:
            logger = self._default_logger
        if logger is not None:
            getattr(logger, level)(msg, *args, **kwargs)
    
    def debug(self, msg, logger=..., *args, **kwargs):
        self._log('debug', msg, logger, *args, **kwargs)
    
    def info(self, msg, logger=..., *args, **kwargs):
        self._log('info', msg, logger, *args, **kwargs)
    
    def warning(self, msg, logger=..., *args, **kwargs):
        self._log('warning', msg, logger, *args, **kwargs)
    
    def error(self, msg, logger=..., *args, **kwargs):
        self._log('error', msg, logger, *args, **kwargs)
    
    def critical(self, msg, logger=..., *args, **kwargs):
        self._log('critical', msg, logger, *args, **kwargs)
    
    def exception(self, msg, logger=..., *args, **kwargs):
        self._log('exception', msg, logger, *args, **kwargs)


logg = LoggerWrapper()

def make_logger(name):
    """
    logger package for user
    Input:
        name: name of the logger
    Output:
        logger object
    """
    logger = getLogger(name)
    if logger is None:
        logger.addHandler(NullHandler())
    logger.setLevel(1) #getting all logs
    #basicConfig(filename='logger.log',filemode='w',level=INFO)

    # determine some max string lengths
    column_length = stty_size()[1]-13
    log_lvl_length = min(max(int(column_length*0.03), 1), 8)
    s1 = '{}.{}s '.format(log_lvl_length, log_lvl_length)
    column_length -= log_lvl_length
    s5 = '-{}.{}s'.format(column_length, column_length)
    
    os.mkdir('logs') if not os.path.exists('logs') else None
    should_roll_over = os.path.isfile('logs/logger.log')
    file_handler = logging.handlers.RotatingFileHandler('logs/logger.log',mode='w' ,maxBytes=1000000, backupCount=3)
    if should_roll_over:  # log already exists, roll over!
        file_handler.doRollover()
    file_handler.setLevel(DEBUG)
    file_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    std_handler = StreamHandler()
    std_handler.setLevel(DEBUG)
    fmt_str = (
        Fore.CYAN + '%(asctime)s' + Fore.RESET + ' │ '
        '%(levelcolor)s%(levelname)-8s' + Fore.RESET + Style.RESET_ALL + ' │ '
        '%(levelcolor)s%(message)s%(reset)s'
    )
    formatter = ColoredFormatter(fmt_str, datefmt='%H:%M:%S')
    std_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(std_handler)

    return logger


logger = make_logger('mb_utils')