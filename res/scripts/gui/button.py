import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageSequence

from res.scripts.config import config, CONST, STRING


class TransButton(ttk.Button):
    def __init__(self, master, **kwargs):
        cmd1 = kwargs.pop('command1', None)
        cmd2 = kwargs.pop('command2', None)

        text1 = kwargs.pop('text1', '')
        text2 = kwargs.pop('text2', '')

        style1 = kwargs.pop('style1', '')
        style2 = kwargs.pop('style2', '')

        super().__init__(master, **kwargs)
        self.__cmds = (cmd1, cmd2)
        self.__texts = (text1, text2)
        self.__styles = (style1, style2)
        self.__status = 0
        self.configure(command=self.on_click, text=self.__texts[self.__status], style=self.__styles[self.__status])

    def transfer(self):
        self.__status = 1 - self.__status
        self.configure(text=self.__texts[self.__status], style=self.__styles[self.__status])

    def on_click(self):
        if callable(self.__cmds[self.__status]) and self.__cmds[self.__status]():
            self.transfer()


class AnimationButton(tk.Button):
    def __init__(self, master, res: str, **kwargs):
        super().__init__(master, **kwargs)

        self.__res = res
        self.__playing = True

        # Loading Image
        img = Image.open(res)
        self.__frames = ImageSequence.all_frames(img)
        self.__index = 0
        cur_frame = ImageTk.PhotoImage(self.__frames[self.__index])
        self.config(image=cur_frame)
        # Need to save the reference, otherwise the image will be gc
        self.__image = cur_frame

        self.after(int(1000 / CONST.LOADING_FRAMERATE), self.__update)

    def __update(self):
        self.after(config.get_int(STRING.CONFIG_UPDATE_INTERVAL), self.__update)
        self.show_next_frame()

    def show_next_frame(self):
        # if not self.__playing:
        #     return

        self.__index = (self.__index + 1) % len(self.__frames)
        cur_frame = ImageTk.PhotoImage(self.__frames[self.__index])
        self.image = cur_frame
        self.config(image=cur_frame)

    def play(self):
        self.__playing = True

    def stop_play(self):
        self.__playing = False
        self.__index = 0
        self.configure(image=ImageTk.PhotoImage(self.__frames[self.__index]))
