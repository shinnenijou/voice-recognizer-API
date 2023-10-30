import time
from threading import Thread, Event
import openai
import requests
from res.scripts.config import config
from res.scripts.config.const import STRING, CONST

class WhisperRecognizer(Thread):
    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()
        self.__src_queue = kwargs.get('src_queue')
        self.__dst_queue = kwargs.get('dst_queue')
        self.__running_flag = _running_flag

    @staticmethod
    def transcribe(_input: str, _language: str):
        audio_file = open(_input, "rb")
        try:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, language=_language)
            return transcript.get('text', '')
        except openai.error.AuthenticationError:
            print(STRING.APIKEY_ERROR)
            return ''

    def fetch_key(self, name: str):
        try:
            resp = requests.get(f"{STRING.BASE_API_URL}/openai_key" , params={"name": name})
            data = resp.json()
            if data.get('code', -2) == 0:
                return data.get('data', '')
            else:
                print("[error]" + data.get('message', 'Unknown error'))
                return ''
        except Exception as e:
            print("[error]" + str(e))
            return ''

    def run(self):
        name = config.get_value(STRING.CONFIG_NAME)
        openai.api_key = self.fetch_key(name)
        while self.__running_flag.is_set():
            if self.__src_queue.empty():
                time.sleep(config.get_int(STRING.CONFIG_UPDATE_INTERVAL) / 1000)
                continue

            file, language = self.__src_queue.get()
            text = self.transcribe(file, language)
            print(text)
            self.__dst_queue.put(text)
