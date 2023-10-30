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

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.__data = {}

    @property
    def data(self):
        return json.dumps(self.__data)

    @data.setter
    def data(self, value: str):
        try:
            data = json.loads(value)
            self.__data = data
        except json.JSONDecodeError as e:
            pass

    def get_data(self, index: int):
        i = 0
        for key, value in self.__data.items():
            if i == index:
                return key, value

            i += 1

    def refresh(self, index: int = 0):
        self.set('')
        options = []

        i = 1
        for key, value in self.__data.items():
            string = f"【{i}】 {key} {value}"
            options.append(string)
            i += 1

        self.config(values=options)

        if len(options) == 0:
            return

        if index >= len(options):
            index = len(options) - 1

        self.current(index)

    def get(self):
        text = super().get()
        if len(text) > 2:
            return int(text[1]) - 1

        return 0
