from threading import Thread, Event

import pyaudio

from res.scripts.config import CONST, STRING


class MicrophoneRecorder(Thread):

    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()

        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(
            format=CONST.FORMAT,
            channels=CONST.CHANNELS,
            rate=CONST.SAMPLING_RATE,
            input=True
        )

        self.__running_flag = _running_flag
        self.__index = 0

        self.__dst_queue = kwargs.get('dst_queue')

    def run(self):
        wave_data = b''
        print(STRING.START_RECOGNIZING)
        while self.__running_flag.is_set():
            # record from microphone
            data = self.__stream.read(CONST.CHUNK_SIZE * 10) # about 0.3s
            self.__dst_queue.put(data)

        self.__stream.stop_stream()
        self.__stream.close()
        self.__audio.terminate()
