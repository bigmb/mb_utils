#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import os
# import subprocess
# import sys
# import shutil


# if sys.version_info[:2] in [(3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14)]:
#     py_requires = f"python{sys.version_info.major}.{sys.version_info.minor}"
# else:
#     py_requires = "python3.8"

# file = os.getcwd() 


# #subprocess.run(["cd",file]), check=True, stdout=subprocess.PIPE).stdout
# os.system('cd ' + file)

# os.system('./make_version.sh')

# print("version file updated")
# print('*'*100)

# # subprocess.run(["git", "add", "."], check=True, stdout=subprocess.PIPE).stdout
# # subprocess.run(["git", "commit", "-am", "Bug fix commit"], check=True, stdout=subprocess.PIPE).stdout

# # print('git commit done')

# subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE).stdout
# print('git pull done')
# print('*'*100)

# subprocess.run(["git", "push"], check=True, stdout=subprocess.PIPE).stdout
# print('*'*100)
# print('removing dist and build folders')


# for folder in ['dist', 'build']:
#     if os.path.exists(folder):
#         shutil.rmtree(folder)
# print('dist/build folders removed')
    

# print('*'*100)

# if subprocess.run(['uv','--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
#     subprocess.run([py_requires, '-m', 'build'], check=True)
#     print('*'*100)
#     subprocess.run([py_requires, '-m', 'pip', 'install', os.path.join('dist', os.listdir('dist')[-1]), '--break-system-packages'], check=True)
#     print('build and installed using pip')
#     print('*'*100)
# else:
#     subprocess.run(['uv', 'build'], check=True)
#     print('*'*100)
#     subprocess.run(['sudo','uv', 'pip', 'install', '--system', os.path.join('dist', os.listdir('dist')[-1])], check=True)
#     print('build and installed using uv')
#     print('*'*100)

# ##Twine upload
# subprocess.run([py_requires, '-m', 'twine', 'upload', 'dist/*'], check=True)

# print('package installed')
# print('*'*100)
# # os.system(py_requires + ' -m twine upload dist/*')


import os
import subprocess
import sys
import glob


def install_package():
    subprocess.run(['./make_version.sh'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    msg = "updated version :" + subprocess.run(['cat', 'VERSION.txt'], check=True, stdout=subprocess.PIPE).stdout.decode().strip()
    # skip commit if make_version.sh already committed everything
    status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(['git', 'commit', '-am', msg], check=True)
        print('git commit done')
    else:
        print('nothing to commit, skipping')
    subprocess.run(['git', 'pull'], check=True)
    print('git pull done')
    subprocess.run(['git', 'push'], check=True)
    subprocess.run(['git', 'push', '--tags'], check=True)
    print('git push done')
    print('*'*100)
    subprocess.run(['rm', '-rf', 'dist'], check=True)
    subprocess.run(['uv', 'build'], check=True)
    latest_file = sorted(os.listdir('./dist'))[-1]
    whl_files = [f for f in os.listdir('./dist') if f.endswith('.whl')]
    latest_file = sorted(whl_files)[-1] if whl_files else sorted(os.listdir('./dist'))[-1]
    print(f'Installing package file: {latest_file}')
    prefix = os.environ.get('MB_UV_PREFIX', os.path.expanduser('~/.local'))
    print(f'Installing into prefix: {prefix}')
    subprocess.run(
        [
            'uv',
            'pip',
            'install',
            f'./dist/{latest_file}',
            '--python',
            sys.executable,
            '--prefix',
            prefix,
        ],
        check=True,
    )
        
        
install_package()
print('package installed')
print('*'*100)
whl_files = glob.glob("dist/*.whl")
subprocess.run(["uvx", "uv-publish"] + whl_files, check=True)

# Upload .whl to the latest GitHub release
version = subprocess.run(['cat', 'VERSION.txt'], capture_output=True, text=True).stdout.strip()
# Create the release if it doesn't exist yet
subprocess.run(['gh', 'release', 'create', version, '--title', f'v{version}', '--notes', f'Release {version}', '--latest'], check=False)
for whl in whl_files:
    subprocess.run(['gh', 'release', 'upload', version, whl, '--clobber'], check=True)
print(f'Uploaded {len(whl_files)} whl file(s) to GitHub release {version}')