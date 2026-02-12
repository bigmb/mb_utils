import subprocess
from typing import Optional
from .logging import logg

__all__ = ['update_package']

def update_package(package_name, logger: Optional[str]=None) -> None:
    # Check if package is up-to-date
    result = subprocess.run(['pip', 'check', package_name], capture_output=True, text=True)
    if 'up-to-date' in result.stdout:        
        logg.info(f"{package_name} is already up-to-date.",logger)
        return
    
    # Install latest version of package
    result = subprocess.run(['pip', 'install', '--upgrade', package_name], capture_output=True, text=True)
    if result.returncode == 0:
        logg.info(f"{package_name} has been updated.",logger)
    else:
        logg.info(f"Error updating {package_name}: {result.stderr}")