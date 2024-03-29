import os

import myPath

from .const import *
from .config import Config, REQUIRE_FIELDS, REMOTE_FIELDS
from .error import *

config = Config(myPath.CONFIG_FILE)


def is_gui_only():
    return os.getenv('GUIONLY', '0') == '1'
