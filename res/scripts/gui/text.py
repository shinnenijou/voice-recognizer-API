import sys

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
