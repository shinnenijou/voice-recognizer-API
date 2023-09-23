import tkinter as tk
from threading import Event as t_Event
from PIL import Image, ImageTk, ImageSequence
from queue import Queue as t_Queue

import myPath
from res.scripts.config import CONST, STRING, ThreadCommand


class LoadingScreen(tk.Tk):
    def __init__(self, flag: t_Event, src_queue: t_Queue):
        super().__init__()
        self.__stop_flag = flag
        self.__text_queue = src_queue
        self.__text = tk.StringVar(value=STRING.LABEL_UPDATE)

        # Loading Image
        img = Image.open(myPath.LOADING_IMG)
        self.__frames = ImageSequence.all_frames(img)
        self.__index = 0

        # Geometry
        width = img.width
        height = img.height

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

        self.__image = tk.Label(self)
        self.__image.place(x=-2, y=-2)

        self.__label_2 = tk.Label(self, textvariable=self.__text, bg="#136dad", fg="#ffffff", font=("Microsoft YaHei UI", "14", "bold"))
        self.__label_2.place(x=275, y=210, anchor="center")

        img.close()
        self.show_next_frame()
        self.after(int(1000 / CONST.LOADING_FRAMERATE), self.__update)

    def __update(self) -> None:
        if self.__stop_flag.is_set():
            self.destroy()
        else:
            self.show_next_frame()
            self.after(int(1000 / CONST.LOADING_FRAMERATE), self.__update)
            while not self.__text_queue.empty():
                cmd, args = self.__text_queue.get()
                self.handle_cmd(cmd, args)

    def show_next_frame(self):
        self.__index = (self.__index + 1) % len(self.__frames)
        cur_frame = ImageTk.PhotoImage(self.__frames[self.__index])
        self.__image.config(image=cur_frame)
        self.__image.image = cur_frame

    def handle_cmd(self, cmd: int, args: list):
        if cmd == ThreadCommand.ShowDownloadProgress:
            self.__text.set(f'{STRING.LABEL_DOWNLOAD}{args[0]}/{args[1]}')
        else:
            pass
