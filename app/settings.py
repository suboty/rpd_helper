import sys

from app.logger import logger


class Settings:
    def __init__(self):
        self.settings = {}

    def set_setting(self, name, value):
        self.settings[name] = value
        logger.debug(f'Setting <{name}> is loaded, '
                     f'type: {type(value)}, '
                     f'size of setting: {sys.getsizeof(value)} bytes, '
                     f'general size: {sys.getsizeof(self.settings)} bytes')

    def get_setting(self, name):
        logger.debug(f'Getting <{name}> from settings...')
        res = self.settings[name]
        logger.debug(f'Getting <{name}> from settings is finish')
        return res


settings = Settings()
