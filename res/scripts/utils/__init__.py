import os
import shutil
import time
from multiprocessing import Queue as p_Queue
from queue import Queue as t_Queue

import myPath


class FileLikeQueue:
    def __init__(self):
        self.__queue = p_Queue(maxsize=0)

    def write(self, data):
        self.__queue.put(data)

    def flush(self):
        pass

    def read(self):
        ret = []
        while not self.__queue.empty():
            ret.append(self.__queue.get())

        return ret


class Logger:
    def __init__(self):
        self.__log_dir = myPath.LOG_PATH

    def init(self, dir_path):
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        self.__log_dir = dir_path

    def log_error(self, msg: str):
        with open(os.path.join(self.__log_dir, f"{get_date()}.log"), "a") as file:
            file.write(f"[{get_hms_time()}][error]{msg}\n")

    def log_info(self,msg: str):
        with open(os.path.join(self.__log_dir, f"{get_date()}.log"), "a") as file:
            file.write(f"[{get_hms_time()}][info]{msg}\n")

    def log_warning(self,msg: str):
        with open(os.path.join(self.__log_dir, f"{get_date()}.log"), "a") as file:
            file.write(f"[{get_hms_time()}][warning]{msg}\n")


class MoveAverage:
    def __init__(self, window: int, threshold: float):
        self.__window = window
        self.__queue = t_Queue(maxsize=0)
        self.__size = 0
        self.__average = 0.0
        self.__sum = 0.0
        self.__range = 1.0
        self.__min = 0.0
        self.__max = 0.0
        self.__detect_threshold = threshold

    def enqueue(self, value: float):
        if self.__size >= self.__window:
            head = self.__queue.get()
            self.__sum -= head
            self.__size -= 1
        elif self.__size == 0 and value > 1 / self.__detect_threshold:
            value = 1 / self.__detect_threshold

        self.__queue.put(value)
        self.__size += 1
        self.__sum += value
        self.__average = self.__sum / self.__size
        self.__max = max(self.__queue.queue)
        self.__min = min(self.__queue.queue)
        self.__range = self.__max - self.__min

        print(f"value: {value}, average: {self.__average}")

    def is_upper_deviation(self, value: float):
        return value > self.__average + self.__range * self.__detect_threshold

    @property
    def average(self):
        return self.__average

    @property
    def max(self):
        return self.__max

    @property
    def min(self):
        return self.__min

    @property
    def range(self):
        return self.__range


def isfile(file_path):
    return os.path.isfile(file_path)


def isdir(dir_path):
    return os.path.isdir(dir_path)


def touch(file_path, content=''):
    if isfile(file_path):
        return

    with open(file_path, 'w') as file:
        file.write(content)


def mkdir(file_path):
    if os.path.isdir(file_path):
        return

    os.mkdir(file_path)


def remove(path: str):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)


def get_hhmmss(seconds: float):
    dec = seconds - int(seconds)
    seconds = int(seconds)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%d:%.2f" % (h, m, s + dec)


def ass_headers():
    text = ""\
         + "[Events]\n" \
         + "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    return text


def ass_event(start: str, end: str, text: str):
    return f"Dialogue: 0,{start},{end},,,0,0,0,,{text}\n"


def rm(file_path):
    os.remove(file_path)


def get_files(path):
    return os.listdir(path)


def get_ms_time():
    return int(time.time() * 1000)


def get_date():
    return time.strftime("%Y-%m-%d", time.gmtime())


def get_hms_time():
    return time.strftime("%H-%M-%S", time.gmtime())


def is_float(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_unit_float(string: str):
    try:
        value = float(string)
        return 0 < value <= 1
    except ValueError:
        return False


class TextFilter:

    def __init__(self):
        self.__ng_words = {}
        if os.path.isfile(os.path.join(myPath.RES_PATH, 'static', 'ng_words.json')):
            import json
            with open(os.path.join(myPath.RES_PATH, 'static', 'ng_words.json'), 'r', encoding='utf-8') as file:
                self.__ng_words = json.loads(file.read())

    def is_legal(self, string: str):
        for key in self.__ng_words.keys():
            if string.find(key) != -1:
                return False

        return True


logger = Logger()
textFilter = TextFilter()
