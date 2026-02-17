
import importlib
from .logging import logg


__all__ = ['check_package']

def check_package(package_name, error_message=None, logger=None):
    """
    Check if a package is installed
    Args:
        package_name (str): Name of the package
        error_message (str, optional): Custom error message to display if the package is not found
        logger (logging.Logger, optional): Logger to use for logging messages
    Returns:
        bool: True if package is installed, False otherwise
    """

    if importlib.util.find_spec(package_name) is not None:
        return True
    else:
        if error_message:
            logg.info(error_message, logger)
        else:
            logg.info(f"Package '{package_name}' not found.", logger)
    return False