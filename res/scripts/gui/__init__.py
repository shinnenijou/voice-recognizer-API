import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from res.scripts.config import CONST, config, STRING
import myPath

from .style import set_style
from .frame import WorkFrame
from .button import TransButton
from .text import WorkText
from .window import *


class MainWindow(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (CONST.WINDOW_WIDTH / 2))
        y = int((screen_height / 2) - (CONST.WINDOW_HEIGHT / 2))

        self.title(STRING.TITLE_MAIN)
        self.iconbitmap(myPath.ICON_IMG)
        self.geometry(f'{CONST.WINDOW_WIDTH}x{CONST.WINDOW_HEIGHT}+{x}+{y}')
        self.resizable(False, False)

        # Main work frame
        self.work_frame = WorkFrame(self, padding=15)
        self.work_frame.pack(expand=True, fill=BOTH)

        # Menu
        menu = ttk.Menu(self)
        self.configure(menu=menu)

        optional_menu = ttk.Menu(menu)
        menu.add_cascade(label=STRING.MENU_OPTIONAL, menu=optional_menu)
        optional_menu.add_command(label=STRING.TITLE_SETTING, command=lambda: pop_setting_window(self))

        help_menu = ttk.Menu(menu)
        menu.add_cascade(label=STRING.MENU_HELP, menu=help_menu)
        help_menu.add_command(label=STRING.TITLE_ABOUT, command=lambda: pop_about_window(self))

    def run(self):
        # override sys callback
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.mainloop()

    def on_exit(self):
        for name, child in self.children.items():
            if hasattr(child, 'on_exit'):
                getattr(child, 'on_exit')()

        self.destroy()

    @staticmethod
    def init_style():
        set_style()
