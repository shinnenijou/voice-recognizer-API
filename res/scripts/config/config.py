from configparser import RawConfigParser
import json

import requests

import myPath
from .. import utils
from .const import STRING

REQUIRE_FIELDS = {
    STRING.CONFIG_AVERAGE_WINDOW: 10,
    STRING.CONFIG_DETECT_THRESHOLD: 0.2,
    STRING.CONFIG_UPDATE_INTERVAL: 100,
    STRING.CONFIG_LANGUAGE: 'ja',
    STRING.CONFIG_MODEL: "large-v2",
    STRING.CONFIG_DEVICE: 'auto',
    STRING.CONFIG_VERSION: '0.2.2',
    STRING.CONFIG_PROXY: '',
    STRING.CONFIG_TIMEOUT: 3,
    STRING.CONFIG_APIKEY: '',
    STRING.CONFIG_CHUNK_NUM: 10,
}


class Config(RawConfigParser):
    def __init__(self, config_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        utils.mkdir(myPath.DATA_DIR)
        utils.touch(config_file, '[global]')
        self.read(config_file, encoding='UTF-8')
        self.__section = self.sections()[0]
        self.__config_file = config_file
        for field, default_value in REQUIRE_FIELDS.items():
            if not self.has_option(self.__section, field):
                self.set_value(field, default_value)

        # some special validata
        if not utils.is_unit_float(self.get_value(STRING.CONFIG_DETECT_THRESHOLD)):
            self.set_value(STRING.CONFIG_DETECT_THRESHOLD, REQUIRE_FIELDS[STRING.CONFIG_DETECT_THRESHOLD])

        self.save()

    def get_value(self, option: str, fallback='') -> str:
        return self.get(self.__section, option, fallback=fallback)

    def get_int(self, option: str, fallback=0) -> int:
        return self.getint(self.__section, option, fallback=fallback)

    def get_float(self, option: str, fallback=0.0) -> float:
        return self.getfloat(self.__section, option, fallback=fallback)

    def get_bool(self, option: str, fallback=False) -> bool:
        return self.getboolean(self.__section, option, fallback=fallback)

    def set_value(self, option: str, value: any):
        self.set(self.__section, option, str(value))

    def save(self):
        with open(self.__config_file, 'w', encoding='UTF-8') as f:
            self.write(f)

    def request_config(self, config_field: str, *args, **kwargs):
        if config_field == STRING.CONFIG_WEBHOOK:
            return self.__request_webhook(*args, **kwargs)

    @staticmethod
    def __request_webhook(*args, **kwargs):
        name = kwargs.get('name', '')
        data = {}

        try:
            resp = requests.get(
                url=f"{STRING.BASE_API_URL}/discord_webhook",
                params={"name": name}
            )

            if resp.status_code == 200:
                data = resp.json().get('data', {})

        except Exception as e:
            print(f"[request_webhook]failed to request webhook_url: {str(e)}")
            pass

        return data
