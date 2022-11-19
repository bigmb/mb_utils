##Function to check paths

import os

def check_path(path,logger=None):
    """
    Function to check the path
    Input:
        path: path to be checked
    Output:
        status: True if the path exists, False otherwise
    """
    status = False
    if os.path.exists(path):
        status = True
    else:
        if logger:
            logger.warning("Path not found : {}".format(path))
    return status