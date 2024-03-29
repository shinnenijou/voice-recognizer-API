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
    STRING.CONFIG_CONFIG_VERSION: 0,
}

REMOTE_FIELDS = {
    STRING.CONFIG_AVERAGE_WINDOW: True,
    STRING.CONFIG_DETECT_THRESHOLD: True,
    STRING.CONFIG_CHUNK_NUM: True,
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

        if option in REMOTE_FIELDS:
            self.set_value(STRING.CONFIG_CONFIG_VERSION, self.get_int(STRING.CONFIG_CONFIG_VERSION) + 1)

    def save(self, config_version=None):
        if config_version is not None:
            self.set_value(STRING.CONFIG_CONFIG_VERSION, config_version)

        with open(self.__config_file, 'w', encoding='UTF-8') as f:
            self.write(f)

    def request_config(self, config_field: str, *args, **kwargs):
        if config_field == STRING.CONFIG_WEBHOOK:
            return self.__get(*args, url=f"{STRING.BASE_API_URL}/discord_webhook/", **kwargs)
        elif config_field == STRING.CONFIG_CHUNK_NUM:
            return self.__get(*args, url=f"{STRING.BASE_API_URL}/fenrir_config/pull/", **kwargs)

    def sync_config(self, config_field: str, *args, **kwargs):
        if config_field == STRING.CONFIG_CHUNK_NUM:
            return self.__post(*args, config_version=self.get_int(STRING.CONFIG_CONFIG_VERSION),
                               url=f"{STRING.BASE_API_URL}/fenrir_config/push/", **kwargs)

    @staticmethod
    def __get(*args, **kwargs):
        name = kwargs.get('name', '')
        url = kwargs.get('url', '')
        data = {}

        try:
            resp = requests.get(
                url=url,
                params={"name": name}
            )

            if resp.status_code == 200:
                data = resp.json().get('data', {})

        except Exception as e:
            print(f"[request_webhook]failed to request webhook_url: {str(e)}")
            pass

        return data

    @staticmethod
    def __post(*arg, **kwargs):
        url = kwargs['url']
        del kwargs['url']
        data = {}

        try:
            resp = requests.post(
                url=url,
                json=kwargs
            )

            if resp.status_code == 200:
                data = resp.json().get('data', {})

        except Exception as e:
            print(f"[request_webhook]failed to request webhook_url: {str(e)}")
            pass

        return data
