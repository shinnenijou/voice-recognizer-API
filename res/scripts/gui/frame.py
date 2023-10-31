import tkinter as tk
import os
from queue import Queue as t_Queue

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import myPath
from res.scripts.config import CONST, is_gui_only, config, STRING
from res.scripts.managers import ThreadManager
from res.scripts.utils import logger

from .button import TransButton, AnimationButton
from .text import WorkText, JsonCombox


class WorkFrame(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.reload_webhook = None

        self.__thread_manager = ThreadManager()
        self.add_threads()

        self.__setting_frame = SettingFrame(self, text=STRING.LABEL_SETTING, padding=10)
        self.__setting_frame.pack(fill=X, expand=YES, anchor=N, side=TOP)
        self.add_options()

        self.__text = WorkText(self, state=NORMAL, cursor='arrow', autohide=True, height=8, takefocus=NO,
                               bootstyle='round', font=CONST.GLOBAL_FONT)
        self.__text.pack(fill=BOTH, expand=YES, pady=10, side=TOP, anchor=N)

        self.__start_button = self.create_start_button()
        self.__start_button.pack()

    # PROPERTIES
    @property
    def thread_manager(self):
        return self.__thread_manager

    # CALLBACK
    def on_exit(self):
        return self.__thread_manager.stop()

    # WORK CONTROL
    def start_threads(self):
        if self.__thread_manager.is_running():
            logger.log_warning("[start_threads]threads has started.")
            return True

        result = False

        try:
            # 保存配置
            self.__text.clear_text()

            self.__setting_frame.save_setting()

            # 如果有输入名字但没有手动获取URL则在启动时主动更新一次
            if not config.get_value(STRING.CONFIG_WEBHOOK) and callable(self.reload_webhook):
                self.reload_webhook()

            result = self.__thread_manager.start()
            if result:
                self.__setting_frame.disable_setting()
        except Exception as e:
            logger.log_error("[start_threads]threads failed to start:" + str(e))

        return result

    def stop_threads(self):
        result = False
        try:
            result = self.__thread_manager.stop()
            if result:
                self.__setting_frame.enable_setting()
        except Exception as e:
            logger.log_error("[stop_threads]threads failed to stop:" + str(e))

        return result

    # WIDGETS
    def add_threads(self):
        if is_gui_only():
            return

        record_queue = t_Queue(maxsize=0)
        voice_queue = t_Queue(maxsize=0)
        text_queue = t_Queue(maxsize=0)

        from res.scripts.stream import MicrophoneRecorder
        self.__thread_manager.add(
            MicrophoneRecorder,
            "Recorder",
            dst_queue=record_queue
        )

        from res.scripts.stream import VoiceDetector
        self.__thread_manager.add(
            VoiceDetector,
            "Detector",
            src_queue=record_queue,
            dst_queue=voice_queue
        )

        from res.scripts.webhook import WebhookSender
        self.__thread_manager.add(
            WebhookSender,
            "Sender",
            src_queue=text_queue
        )

        from res.scripts.recognize import WhisperRecognizer
        self.__thread_manager.add(
            WhisperRecognizer,
            "Recognizer",
            src_queue=voice_queue,
            dst_queue=text_queue,
        )

    def add_options(self):
        name_frame = ttk.Frame(self.__setting_frame)
        name_frame.pack(fill=X, expand=YES, pady=(2.5, 2.5))
        ttk.Label(name_frame, text=STRING.LABEL_NAME, width=15).pack(side=LEFT, padx=(15, 0))
        name_entry = ttk.Entry(name_frame, name=STRING.CONFIG_NAME)
        name_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)
        name_entry.insert(0, config.get_value(STRING.CONFIG_NAME))

        url_frame = ttk.Frame(self.__setting_frame)
        url_frame.pack(fill=X, expand=YES, pady=(0, 2.5))
        ttk.Label(url_frame, text=STRING.LABEL_WEBHOOK, width=15).pack(side=LEFT, padx=(15, 0))
        url_combobox = JsonCombox(url_frame, name=STRING.CONFIG_WEBHOOK, state=READONLY)
        url_combobox.pack(side=LEFT, fill=X, expand=YES, padx=5)
        reload_button = ttk.Button(url_frame, text=STRING.BUTTON_FETCH, takefocus=False)
        reload_button.pack(side=RIGHT, padx=(0, 15))

        language_frame = ttk.Frame(self.__setting_frame)
        language_frame.pack(fill=X, expand=YES, pady=(10, 0))
        ttk.Label(language_frame, text=STRING.LABEL_LANGUAGE, width=15).pack(side=LEFT, padx=(15, 15))
        for text, language in STRING.LANGUAGE_MAP.items():
            button = ttk.Radiobutton(language_frame, text=text, value=language,
                                     variable=self.__setting_frame.language_var)
            button.pack(side=LEFT, padx=(0, 15))
            if language == config.get_value(STRING.CONFIG_LANGUAGE):
                button.invoke()

        # 注册需要的闭包
        def reload_webhook():
            url_combobox.data = config.request_config(STRING.CONFIG_WEBHOOK, name=name_entry.get())
            url_combobox.refresh()

        self.reload_webhook = reload_webhook
        self.reload_webhook()
        reload_button.config(command=self.reload_webhook)

    def create_start_button(self):
        return TransButton(
            self,
            command1=self.start_threads,
            command2=self.stop_threads,
            text1=STRING.BUTTON_START,
            text2=STRING.BUTTON_STOP,
            style1='primary.TButton',
            style2='danger.TButton',
            width=10,
            takefocus=False
        )


class SettingFrame(ttk.Labelframe):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.language_var = ttk.StringVar()

    def enable_setting(self):
        for _, frame in self.children.items():
            for name, widget in frame.children.items():
                if isinstance(widget, ttk.Entry):
                    widget.configure(state=NORMAL)
                elif isinstance(widget, ttk.Combobox):
                    widget.configure(state=NORMAL)
                elif isinstance(widget, ttk.Radiobutton):
                    widget.configure(state=NORMAL)

    def disable_setting(self):
        for _, frame in self.children.items():
            for name, widget in frame.children.items():
                if isinstance(widget, ttk.Entry):
                    widget.configure(state=DISABLED)
                elif isinstance(widget, ttk.Combobox):
                    widget.configure(state=DISABLED)
                elif isinstance(widget, ttk.Radiobutton):
                    widget.configure(state=DISABLED)

    def save_setting(self):
        for _, frame in self.children.items():
            for name, widget in frame.children.items():
                if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
                    config.set_value(name, widget.get())

        config.set_value(STRING.CONFIG_LANGUAGE, self.language_var.get())

        config.save()
