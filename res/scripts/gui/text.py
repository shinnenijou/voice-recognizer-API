import sys
import json

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

from res.scripts.config import STRING, config


class WorkText(ScrolledText):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # register update
        self.__update_interval = config.get_int(STRING.CONFIG_UPDATE_INTERVAL)
        self.after(self.__update_interval, self.__update)

    def __update(self) -> None:
        self.after(self.__update_interval, self.__update)

        texts = sys.stdout.read()
        self.text.configure(state=NORMAL)
        for text in texts:
            if text == '':
                continue

            self.text.insert(END, text)
            self.text.see(END)

        self.text.configure(state=DISABLED)

    def clear_text(self):
        self.text.configure(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.configure(state=DISABLED)


class JsonCombox(ttk.Combobox):
    SEP = ':'

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.__data = {}

    @property
    def data(self):
        return json.dumps(self.__data)

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            return

        self.__data = value

    def get_data(self, index: int):
        i = 0
        for key, value in self.__data.items():
            if i == index:
                return key, value

            i += 1

    def refresh(self):
        self.set('')
        url = config.get_value(STRING.CONFIG_WEBHOOK, '')
        index = -1

        options = []
        i = 0
        for key, value in self.__data.items():
            string = f"{key}{self.SEP} {value}"
            options.append(string)

            if value == url.strip():
                index = i

            i += 1

        self.config(values=options)

        if len(options) == 0:
            return

        if index == -1:
            index = 0

        self.current(index)

    def get(self):
        text = super().get()
        index = text.find(self.SEP)

        if index != 1:
            return text[index+1:].strip()

        return ''
