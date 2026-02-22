## file for reading yaml files

import yaml
from .logging import logg

__all__ = ['read_yaml']

def read_yaml(file_path,logger=None):
    '''
    Reads a yaml file and returns the data as a dictionary.
    Args:
        file_path (str): The path to the yaml file.
        logger (logging.Logger, optional): Logger for logging messages. Defaults to None.
    Returns:
        dict: The data from the yaml file.
    '''
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    logg.info(f"yaml file read successfully from {file_path}", logger)
    return data