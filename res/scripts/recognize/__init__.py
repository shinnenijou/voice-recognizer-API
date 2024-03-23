import time
from threading import Thread, Event
import openai
import requests
from res.scripts.config import config
from res.scripts.config.const import STRING, CONST
from res.scripts.utils import textFilter


class WhisperRecognizer(Thread):
    def __init__(self, _running_flag: Event, **kwargs):
        super().__init__()
        self.__src_queue = kwargs.get('src_queue')
        self.__dst_queue = kwargs.get('dst_queue')
        self.__running_flag = _running_flag
        self.client: openai.OpenAI | None = None

    def transcribe(self, _input: str, _language: str):
        audio_file = open(_input, "rb")
        try:
            transcript = self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                language=_language,
            )
            return transcript.get('text', '')
        except openai.AuthenticationError:
            print(STRING.APIKEY_ERROR)
            return ''

    @staticmethod
    def fetch_key(name: str):
        try:
            resp = requests.get(f"{STRING.BASE_API_URL}/openai_key", params={"name": name})
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

        api_key = self.fetch_key(name)

        self.client = openai.OpenAI(
            api_key=api_key,
            timeout=config.get_float(STRING.CONFIG_TIMEOUT),
        )

        # 请求速率控制
        request_interval = 60000 / CONST.WHISPER_RPM
        last_request_time = 0

        while self.__running_flag.is_set():
            if self.__src_queue.empty():
                time.sleep(config.get_int(STRING.CONFIG_UPDATE_INTERVAL) / 1000)
                continue

            current_time = time.time() * 1000

            if current_time - last_request_time < request_interval:
                print("waiting: ", (request_interval - current_time + last_request_time) / 1000, " seconds")
                time.sleep((request_interval - current_time + last_request_time) / 1000)

            file, language = self.__src_queue.get()
            text = self.transcribe(file, language)

            if not textFilter.is_legal(text):
                continue

            print(text)
            self.__dst_queue.put(text)
