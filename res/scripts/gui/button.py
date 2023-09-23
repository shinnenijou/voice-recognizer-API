import ttkbootstrap as ttk


class TransButton(ttk.Button):
    def __init__(self, master, **kwargs):
        cmd1 = kwargs.pop('command1', None)
        cmd2 = kwargs.pop('command2', None)

        text1 = kwargs.pop('text1', '')
        text2 = kwargs.pop('text2', '')

        style1 =  kwargs.pop('style1', '')
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