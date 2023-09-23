from threading import Thread, Event
import gc
from res.scripts.config import EResult, ErrorString
from res.scripts.utils import logger


class ThreadManager:

    def __init__(self):
        self.__running_flag = Event()
        self.__tasks = []
        self.__templates = {}
        self.__threads = {}
        self.__args = {}
        self.__queue_ref = []

    def is_running(self):
        return self.__running_flag.is_set()

    def add(self, template, name:str, **kwargs):
        if self.__running_flag.is_set():
            return False

        if not issubclass(template, Thread):
            return False

        if name in self.__tasks:
            return False

        self.__tasks.append(name)
        self.__args[name] = kwargs
        self.__templates[name] = template

        if 'dst_queue' in kwargs:
            self.__queue_ref.append(kwargs.get('dst_queue'))

        if 'src_queue' in kwargs:
            self.__queue_ref.append(kwargs.get('src_queue'))

        return True

    def remove(self, name:str):
        if self.__running_flag.is_set():
            return False

        if name in self.__tasks:
            self.__tasks.remove(name)
            del self.__args[name]
            del self.__templates[name]

        return True

    def start(self):
        if self.__running_flag.is_set():
            return False

        for queue in self.__queue_ref:
            while not queue.empty():
                queue.get()

        for thread_name in self.__tasks:
            self.__threads[thread_name] = self.__templates[thread_name](self.__running_flag, **self.__args[thread_name])

            result = EResult.Success
            if hasattr(self.__threads[thread_name], 'init'):
                result = self.__threads[thread_name].init()

            if result != EResult.Success:
                self.__clear()
                logger.log_error(f"{thread_name} init failed: " + ErrorString.get(result, ""))

                return False

        self.__running_flag.set()

        for thread_name in self.__tasks:
            self.__threads[thread_name].start()

        return True

    def stop(self):
        if not self.__running_flag.is_set():
            return False

        self.__running_flag.clear()

        for thread_name in self.__tasks:
            if thread_name in self.__threads:
                self.__threads[thread_name].join()
                del self.__threads[thread_name]

        for queue in self.__queue_ref:
            while not queue.empty():
                queue.get()

        return True

    def __clear(self):
        for thread_name in self.__tasks:
            if thread_name in self.__threads:
                del self.__threads[thread_name]

        gc.collect()