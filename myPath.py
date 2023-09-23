from os.path import join, dirname

# DIR
ROOT_PATH = dirname(__file__)
LOG_PATH = join(ROOT_PATH, 'logs')
RES_PATH = join(ROOT_PATH, 'res')
ENV_PATH = join(ROOT_PATH, 'env')
TEMP_PATH = join(ROOT_PATH, '.temp')
PYTHON_PATH = join(ENV_PATH, 'python.exe')
MODEL_PATH = join(RES_PATH, 'model')
SCRIPTS_PATH = join(RES_PATH, 'scripts')
IMG_RES_PATH = join(RES_PATH, 'img')
AUDIO_RES_PATH = join(RES_PATH, 'audio')

# FILE
CONFIG_FILE = join(ROOT_PATH, 'config.ini')

# AUDIO
LOADING_WAV = join(AUDIO_RES_PATH, 'kamome.wav')

# IMG
LOADING_IMG = join(IMG_RES_PATH, 'loading.gif')
LOGO_IMG = join(IMG_RES_PATH, 'logo.png')
ICON_IMG = join(IMG_RES_PATH, 'icon.ico')
