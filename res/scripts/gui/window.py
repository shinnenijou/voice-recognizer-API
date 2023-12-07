import os

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tktooltip import ToolTip

from res.scripts.config import CONST, config, STRING, REQUIRE_FIELDS
import res.scripts.utils as utils
import myPath


def pop_about_window(master):
    win = ttk.Toplevel(master=master, title=STRING.TITLE_ABOUT)

    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = int((screen_width / 2) - (CONST.ABOUT_WIDTH / 2))
    y = int((screen_height / 2) - (CONST.ABOUT_HEIGHT / 2))
    win.geometry(f'{CONST.ABOUT_WIDTH}x{CONST.ABOUT_HEIGHT}+{x}+{y}')
    win.resizable(False, False)

    about_frame = ttk.Frame(win, padding=5)
    about_frame.pack(fill=BOTH, expand=YES)

    # Logo
    logo_frame = ttk.Frame(about_frame)
    logo_frame.pack(side=LEFT)
    img = ttk.Image.open(myPath.LOGO_IMG)
    photo = ttk.ImageTk.PhotoImage(img)
    label = ttk.Label(logo_frame, image=photo)
    label.image = photo
    label.pack(side=TOP)
    img.close()

    # Version
    ttk.Label(logo_frame, text=f'Version: {config.get_value(STRING.CONFIG_VERSION)}').pack()
    ttk.Label(logo_frame, text=f'Author: {STRING.LABEL_AUTHOR}').pack()

    # Story
    label_frame = ttk.Labelframe(about_frame, text=STRING.LABEL_STORY_TITLE)
    label_frame.pack(fill=BOTH, expand=YES, side=RIGHT)
    ttk.Label(label_frame, text=STRING.LABEL_STORY_TEXT, font=CONST.GLOBAL_FONT, justify=CENTER).pack()


def pop_setting_window(master):
    win = ttk.Toplevel(master=master, title=STRING.TITLE_SETTING)
    win.resizable(False, False)

    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = int((screen_width / 2) - (CONST.ABOUT_WIDTH / 2))
    y = int((screen_height / 2) - (CONST.ABOUT_HEIGHT / 2))
    win.geometry(f'{CONST.ABOUT_WIDTH}x{CONST.ABOUT_HEIGHT}+{x}+{y}')

    setting_frame = ttk.Frame(win, padding=15)
    setting_frame.pack(fill=BOTH, expand=YES)

    # PROXY
    proxy_frame = ttk.Frame(setting_frame)
    proxy_frame.pack(side=TOP, fill=X, expand=YES, pady=(5, 2.5))
    proxy_label_var = ttk.StringVar(proxy_frame, value=STRING.LABEL_PROXY)
    proxy_entry_var = ttk.StringVar(proxy_frame, name=STRING.CONFIG_PROXY, value=config.get_value(STRING.CONFIG_PROXY))
    ttk.Label(proxy_frame, textvariable=proxy_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    proxy_entry = ttk.Entry(proxy_frame, textvariable=proxy_entry_var)
    proxy_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
    ToolTip(proxy_entry, STRING.TIP_PROXY, delay=0.5, follow=False)

    proxy_entry_var.trace_add('write', lambda a, b, c: proxy_label_var.set(STRING.LABEL_PROXY+STRING.LABEL_MODIFY_MARK))

    # TIMEOUT
    timeout_frame = ttk.Frame(setting_frame)
    timeout_frame.pack(side=TOP, fill=X, expand=YES, pady=(5, 2.5))
    timeout_label_var = ttk.StringVar(timeout_frame, value=STRING.LABEL_TIMEOUT)
    timeout_entry_var = ttk.StringVar(timeout_frame, name=STRING.CONFIG_TIMEOUT, value=config.get_value(STRING.CONFIG_TIMEOUT))
    ttk.Label(timeout_frame, textvariable=timeout_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    timeout_entry = ttk.Entry(timeout_frame, textvariable=timeout_entry_var)
    timeout_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
    timeout_entry_var.trace_add('write', lambda a, b, c: timeout_label_var.set(STRING.LABEL_TIMEOUT+STRING.LABEL_MODIFY_MARK))

    # DETECT THRESHOLD
    threshold_frame = ttk.Frame(setting_frame)
    threshold_frame.pack(side=TOP, fill=X, expand=YES, pady=(5, 2.5))
    threshold_label_var = ttk.StringVar(threshold_frame, value=STRING.LABEL_DETECT_THRESHOLD)
    threshold_entry_var = ttk.StringVar(threshold_frame, name=STRING.CONFIG_DETECT_THRESHOLD, value=config.get_value(STRING.CONFIG_DETECT_THRESHOLD))
    ttk.Label(threshold_frame, textvariable=threshold_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    threshold_entry = ttk.Entry(threshold_frame, textvariable=threshold_entry_var, validate="focus")
    threshold_entry.configure(validatecommand=lambda: utils.is_unit_float(threshold_entry.get()))
    threshold_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
    ToolTip(threshold_entry, STRING.TIP_DETECT_THRESHOLD, delay=0.5, follow=False)
    threshold_entry_var.trace_add('write', lambda a, b, c: threshold_label_var.set(STRING.LABEL_DETECT_THRESHOLD+STRING.LABEL_MODIFY_MARK))

    # average_window
    average_window_frame = ttk.Frame(setting_frame)
    average_window_frame.pack(side=TOP, fill=X, expand=YES, pady=(5, 2.5))
    average_window_label_var = ttk.StringVar(average_window_frame, value=STRING.LABEL_AVERAGE_WINDOW)
    average_window_entry_var = ttk.StringVar(average_window_frame, name=STRING.CONFIG_AVERAGE_WINDOW, value=config.get_value(STRING.CONFIG_AVERAGE_WINDOW))
    ttk.Label(average_window_frame, textvariable=average_window_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    average_window_entry = ttk.Entry(average_window_frame, textvariable=average_window_entry_var)
    average_window_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
    average_window_entry_var.trace_add('write', lambda a, b, c: average_window_label_var.set(STRING.LABEL_AVERAGE_WINDOW+STRING.LABEL_MODIFY_MARK))

    # chunk_num
    chunk_num_frame = ttk.Frame(setting_frame)
    chunk_num_frame.pack(side=TOP, fill=X, expand=YES, pady=(5, 2.5))
    chunk_num_label_var = ttk.StringVar(chunk_num_frame, value=STRING.LABEL_CHUNK_NUM)
    chunk_num_entry_var = ttk.StringVar(chunk_num_frame, name=STRING.CONFIG_CHUNK_NUM, value=config.get_value(STRING.CONFIG_CHUNK_NUM))
    ttk.Label(chunk_num_frame, textvariable=chunk_num_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    chunk_num_entry = ttk.Entry(chunk_num_frame, textvariable=chunk_num_entry_var)
    chunk_num_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
    chunk_num_entry_var.trace_add('write', lambda a, b, c: chunk_num_label_var.set(STRING.LABEL_CHUNK_NUM+STRING.LABEL_MODIFY_MARK))

    # setting dict
    settings = {
        STRING.CONFIG_PROXY: proxy_entry_var,
        STRING.CONFIG_DETECT_THRESHOLD: threshold_entry_var,
        STRING.CONFIG_TIMEOUT: timeout_entry_var,
        STRING.CONFIG_AVERAGE_WINDOW: average_window_entry_var,
        STRING.CONFIG_CHUNK_NUM: chunk_num_entry_var,
    }
    labels = {
        STRING.CONFIG_PROXY: proxy_label_var,
        STRING.CONFIG_DETECT_THRESHOLD: threshold_label_var,
        STRING.CONFIG_TIMEOUT: timeout_label_var,
        STRING.CONFIG_AVERAGE_WINDOW: average_window_label_var,
        STRING.CONFIG_CHUNK_NUM: chunk_num_label_var
    }

    # Confirm BUTTON
    def save_setting():
        if Messagebox.show_question(message=STRING.CONFIRM_SETTING_MODIFY, title=STRING.LABEL_SAVE,
                                    buttons=[f'{STRING.LABEL_YES}:primary', f'{STRING.LABEL_NO}:secondary'],
                                    parent=win, alert=False) == STRING.LABEL_YES:

            for name, widget in settings.items():
                config.set_value(name, widget.get())

            for name, widget in labels.items():
                if widget.get()[-1] == STRING.LABEL_MODIFY_MARK:
                    widget.set(widget.get()[:-1])

            # some special validate
            if not utils.is_unit_float(config.get_value(STRING.CONFIG_DETECT_THRESHOLD)):
                config.set_value(STRING.CONFIG_DETECT_THRESHOLD, REQUIRE_FIELDS[STRING.CONFIG_DETECT_THRESHOLD])

            config.save()
            win.destroy()

    def on_exit():
        for name, widget in labels.items():
            if widget.get()[-1] == STRING.LABEL_MODIFY_MARK:
                save_setting()
                break

        win.destroy()

    button_frame = ttk.Frame(setting_frame)
    button_frame.pack(side=TOP, fill=X, expand=YES, pady=(2.5, 5))
    ttk.Button(button_frame, width=10, text=STRING.LABEL_SAVE, command=save_setting).pack(side=LEFT, padx=(40, 7.5))
    ttk.Button(button_frame, width=10, text=STRING.LABEL_CANCEL, command=win.destroy).pack(side=RIGHT, padx=(7.5, 40))

    win.protocol("WM_DELETE_WINDOW", on_exit)
