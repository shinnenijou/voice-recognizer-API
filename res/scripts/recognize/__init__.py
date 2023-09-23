import os
import sys
from multiprocessing import Event
import openai
from res.scripts.config.const import STRING


class WhisperRecognizer:
    def __init__(self, **kwargs):
        self.__key = kwargs.get("api_key")
        self.__src_queue = kwargs.get('src_queue')
        self.__dst_queue = kwargs.get('dst_queue')
        if kwargs.get('proxy', ''):
            os.putenv('http_proxy', kwargs.get('proxy'))
            os.putenv('https_proxy', kwargs.get('proxy'))

    def init(self):
        openai.api_key = self.__key

    @staticmethod
    def transcribe(_input: str, _language: str):
        audio_file = open(_input, "rb")
        try:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, language=_language)
            return transcript.get('text', '')
        except openai.error.AuthenticationError:
            print(STRING.APIKEY_ERROR)
            return ''

    def run(self, running_flag: Event, output):
        sys.stdout = output
        sys.stderr = output
        self.init()
        running_flag.set()

        while True:
            file, language = self.__src_queue.get()
            text = self.transcribe(file, language)
            print(text)
            self.__dst_queue.put(text)