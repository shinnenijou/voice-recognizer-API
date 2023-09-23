import sys
import os
from threading import Thread, Event as t_Event
from queue import Queue as t_Queue

import myPath
from res.scripts.loading import check_update
from res.scripts.utils import FileLikeQueue, mkdir, remove, logger
from res.scripts.config import ThreadCommand, config, STRING


# GLOBAL
p_recognizer = None
output = FileLikeQueue()
loading_screen = None

def loading(is_complete: t_Event, is_reboot: t_Event, queue: t_Queue):
    global p_recognizer
    global loading_screen
    global output

    try:
        # update resource
        if check_update(queue):
            is_reboot.set()
    except Exception as e:
        logger.log_error(f"[check_update]now version: {config.get_value(STRING.CONFIG_VERSION)}, update failed: " + str(e))

    is_complete.set()


def main():
    global loading_screen

    # init log
    logger.init(myPath.LOG_PATH)

    # Redirect standard output
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = output
    sys.stderr = output
    mkdir(myPath.TEMP_PATH)

    # SET PROXY
    if config.get_value(STRING.CONFIG_PROXY):
        os.putenv('http_proxy', config.get_value(STRING.CONFIG_PROXY))
        os.putenv('https_proxy', config.get_value(STRING.CONFIG_PROXY))

    # start loading screen
    from res.scripts.loading import LoadingScreen
    complete_flag = t_Event()
    reboot_flag = t_Event()
    queue_loading = t_Queue()
    t_loading = Thread(target=loading, args=(complete_flag, reboot_flag, queue_loading, ))
    loading_screen = LoadingScreen(complete_flag, queue_loading)
    loading_screen.overrideredirect(True)
    t_loading.start()
    loading_screen.mainloop()
    t_loading.join()

    # Reboot after updating
    if reboot_flag.is_set():
        exit(ThreadCommand.RebootExitCode)

    # Main GUI Process, Threads will be managed in Main Process
    from res.scripts.gui import MainWindow
    win = MainWindow(themename='yeti')

    # start main window
    win.init_style()
    win.run()

    # Exit
    remove(myPath.TEMP_PATH)
    sys.stdout = save_stdout
    sys.stderr = save_stderr


if __name__ == '__main__':
    main()
