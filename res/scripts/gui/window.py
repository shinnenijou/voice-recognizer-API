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

    # MODEL
    model_frame = ttk.Frame(setting_frame)
    model_frame.pack(side=TOP, fill=X, expand=YES, pady=(2.5, 2.5))
    model_label_var = ttk.StringVar(model_frame, value=STRING.LABEL_MODEL)
    model_menu_var = ttk.StringVar(model_frame, name=STRING.CONFIG_MODEL, value=config.get_value(STRING.CONFIG_MODEL))
    model_menu_var.trace_add('write', lambda a, b, c: model_label_var.set(STRING.LABEL_MODEL+STRING.LABEL_MODIFY_MARK))
    ttk.Label(model_frame, textvariable=model_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    model_button = ttk.Menubutton(model_frame, style='primary.Outline.TMenubutton', textvariable=model_menu_var)
    model_menu = ttk.Menu(model_button)
    for option in os.listdir(myPath.MODEL_PATH):
        model_menu.add_radiobutton(label=option, value=option, variable=model_menu_var)
    model_button.configure(menu=model_menu)
    model_button.pack(side=LEFT, fill=X, expand=YES, padx=5)

    # DEVICE
    device_frame = ttk.Frame(setting_frame)
    device_frame.pack(side=TOP, fill=X, expand=YES, pady=(2.5, 2.5))
    device_label_var = ttk.StringVar(device_frame, value=STRING.LABEL_DEVICE)
    device_menu_var = ttk.StringVar(device_frame, name=STRING.CONFIG_DEVICE, value=config.get_value(STRING.CONFIG_DEVICE))
    device_menu_var.trace_add('write', lambda a, b, c: device_label_var.set(STRING.LABEL_DEVICE+STRING.LABEL_MODIFY_MARK))
    ttk.Label(device_frame, textvariable=device_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    device_button = ttk.Menubutton(device_frame, style='primary.Outline.TMenubutton', textvariable=device_menu_var)
    device_menu = ttk.Menu(device_button)
    for option in CONST.DEVICE_LIST:
        device_menu.add_radiobutton(label=option, value=option, variable=device_menu_var)
    device_button.configure(menu=device_menu)
    device_button.pack(side=LEFT, fill=X, expand=YES, padx=5)

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
    proxy_entry_var.trace_add('write', lambda a, b, c: proxy_label_var.set(STRING.LABEL_DETECT_THRESHOLD+STRING.LABEL_MODIFY_MARK))

    # TIMEOUT
    timeout_frame = ttk.Frame(setting_frame)
    timeout_frame.pack(side=TOP, fill=X, expand=YES, pady=(5, 2.5))
    timeout_label_var = ttk.StringVar(timeout_frame, value=STRING.LABEL_TIMEOUT)
    timeout_entry_var = ttk.StringVar(timeout_frame, name=STRING.CONFIG_TIMEOUT, value=config.get_value(STRING.CONFIG_TIMEOUT))
    ttk.Label(timeout_frame, textvariable=timeout_label_var, width=15).pack(side=LEFT, padx=(15, 0))
    timeout_entry = ttk.Entry(timeout_frame, textvariable=timeout_entry_var)
    timeout_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
    proxy_entry_var.trace_add('write', lambda a, b, c: proxy_label_var.set(STRING.LABEL_TIMEOUT+STRING.LABEL_MODIFY_MARK))

    # setting dict
    settings = {
        STRING.CONFIG_PROXY: proxy_entry_var,
        STRING.CONFIG_MODEL: model_menu_var,
        STRING.CONFIG_DEVICE: device_menu_var,
        STRING.CONFIG_DETECT_THRESHOLD: threshold_entry_var,
        STRING.CONFIG_TIMEOUT: timeout_entry_var,
    }
    labels = {
        STRING.CONFIG_PROXY: proxy_label_var,
        STRING.CONFIG_MODEL: model_label_var,
        STRING.CONFIG_DEVICE: device_label_var,
        STRING.CONFIG_DETECT_THRESHOLD: threshold_label_var,
        STRING.CONFIG_TIMEOUT: timeout_label_var,
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
