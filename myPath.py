import os
from os.path import join, dirname

# DIR
__APPDATA__ = os.getenv('APPDATA')
DATA_DIR = os.path.join(__APPDATA__, 'FenrirChan')
LOG_PATH = join(DATA_DIR, 'logs')
TEMP_PATH = join(DATA_DIR, 'temp')
CONFIG_FILE = join(DATA_DIR, 'config.ini')

WORK_DIR = dirname(__file__)
RES_PATH = join(WORK_DIR, 'res')
ENV_PATH = join(WORK_DIR, 'env')
PYTHON_PATH = join(ENV_PATH, 'python.exe')
SCRIPTS_PATH = join(RES_PATH, 'scripts')
IMG_RES_PATH = join(RES_PATH, 'img')
AUDIO_RES_PATH = join(RES_PATH, 'audio')

# AUDIO
LOADING_WAV = join(AUDIO_RES_PATH, 'kamome.wav')

# IMG
LOADING_IMG = join(IMG_RES_PATH, 'loading.gif')
LOGO_IMG = join(IMG_RES_PATH, 'logo.png')
ICON_IMG = join(IMG_RES_PATH, 'icon.ico')
