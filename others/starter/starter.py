import os
import subprocess

WORK_DIR = os.path.dirname(os.path.dirname(__file__))
PYTHON_EXE = os.path.abspath(os.path.join(WORK_DIR, 'env', 'python.exe'))
MAIN_FILE = os.path.abspath(os.path.join(WORK_DIR, 'main.py'))

while True:
    subp = subprocess.run(f'"{PYTHON_EXE}" -B -s "{MAIN_FILE}"', shell=True)
    if subp.returncode != 100:
        break
