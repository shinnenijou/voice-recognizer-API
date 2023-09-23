import wave
import os
import time
from threading import Thread, Event
from queue import Queue as t_Queue

import pyaudio
import torch

import myPath
from res.scripts import utils
from res.scripts.config import CONST, config, STRING


SAMPLING_RATE = 16000
torch.set_num_threads(1)


class VoiceDetector(Thread):
    class State:
        Voice = 1
        Silent = 2

    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()
        self.__model, model_utils = torch.hub.load(
            repo_or_dir=os.path.join(myPath.dirname(__file__), "silero-vad"),
            model='silero_vad',
            force_reload=True,
            source='local'
        )

        (self.__get_speech_timestamps,
         self.__save_audio,
         self.__read_audio,
         self.__VADIterator,
         self.__collect_chunks) = model_utils

        self.__data_queue = t_Queue(maxsize=0)
        self.__state = self.State.Silent

        self.__average_prob = utils.MoveAverage(config.get_int(STRING.CONFIG_AVERAGE_WINDOW))
        self.__detect_threshold = 1 / config.get_float(STRING.CONFIG_DETECT_THRESHOLD)

        self.__index = 0
        self.__running_flag = _running_flag
        self.__src_queue: t_Queue = kwargs.get('src_queue')
        self.__dst_queue: t_Queue = kwargs.get('dst_queue')

    def predict_probability(self, file):
        wav = self.__read_audio(file, sampling_rate=SAMPLING_RATE)
        return self.__model(wav, SAMPLING_RATE).item()

    def run(self):
        wave_data = b''
        while self.__running_flag.is_set():
            if self.__src_queue.empty():
                time.sleep(config.get_int(STRING.CONFIG_UPDATE_INTERVAL) / 1000)
                continue

            data = self.__src_queue.get()
            file = self.save_waveform(data)

            # predict voice probability
            prob = self.predict_probability(file)
            utils.rm(file)

            # State machine
            if self.__state == self.State.Silent:
                if self.__average_prob.is_upper_deviation(prob, self.__detect_threshold):
                    # 疑似发言, 加入数据队列并转变状态
                    self.__data_queue.put(data)
                    self.__state = self.State.Voice
                else:
                    # 在底噪偏差范围内, 计入底噪, 数据入队，状态不变
                    self.__average_prob.enqueue(prob)

                    while not self.__data_queue.empty():
                        self.__data_queue.get()

                    self.__data_queue.put(data)
            else:
                if self.__average_prob.is_upper_deviation(prob, self.__detect_threshold):
                    # 疑似发言, 加入数据队列, 状态不变
                    self.__data_queue.put(data)
                else:
                    # 在底噪偏差范围内, 计入底噪, 加入数据队列, 转变状态, 整合数据并输出
                    self.__data_queue.put(data)
                    self.__average_prob.enqueue(prob)

                    blob = b''
                    while not self.__data_queue.empty():
                        blob += self.__data_queue.get()

                    file = self.save_waveform(blob)
                    self.__dst_queue.put((file, config.get_value(STRING.CONFIG_LANGUAGE)))

                    self.__state = self.State.Silent

    def save_waveform(self, data: bytes):
        self.__index = self.__index + 1
        file = os.path.join(myPath.TEMP_PATH, f'{self.__index}.wav')
        with wave.open(file, 'wb') as wf:
            wf.setnchannels(CONST.CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(CONST.FORMAT))
            wf.setframerate(CONST.SAMPLING_RATE)
            wf.writeframes(data)

        return file
