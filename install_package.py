#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##Run the make_version file to update the version number and then run this file to install the package and upload it to pipy.

import os
import subprocess
file = '/home/malav/basic_mb'

#subprocess.run(["cd",file]), check=True, stdout=subprocess.PIPE).stdout
os.system('cd ' + file)

os.system('./make_version.sh')

print("version file updated")

if os.path.exists(file+'/dist'):
    os.system('sudo rm -rf '+file+'/dist')
    os.system('sudo rm -rf '+file+'/build')
#subprocess.run(["ls"]),check=True, stdout=subprocess.PIPE).stdout
os.system("ls")
subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE).stdout
#os.system('git pull')
print('git pull done')
print('*'*100)
os.system('python3.8 -m setup bdist_wheel')

print('*'*100)
print('wheel built')
os.system('python3.8 -m pip install '+file + '/dist/' +os.listdir(file +'/dist')[-1])

print('package installed')
print('*'*100)
os.system('python3.8 -m twine upload dist/*')
