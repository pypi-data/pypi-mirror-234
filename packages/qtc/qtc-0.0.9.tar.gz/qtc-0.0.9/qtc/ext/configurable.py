import yaml
from qtc.ext.logging import set_logger
logger = set_logger()


class Configurable:
    DEFAULT_CONFIG = dict()

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config):
        self.__config = config

    def update_config(self, **kwargs):
        config = self.DEFAULT_CONFIG.copy()
        config.update(self.config)

        keys_config = set()
        keys_non_config = set()
        for key, value in kwargs.items():
            if key not in config:
                logger.debug(f'keyword={key} in kwargs not recognized in default_config !')
                keys_non_config.add(key)
            else:
                keys_config.add(key)

        config.update(kwargs)
        self.config = config.copy()

        return keys_config, keys_non_config

    def reset_config(self):
        self.config = self.DEFAULT_CONFIG.copy()

    def _read_config(self, config):
        if isinstance(config, str):
            try:
                with open(config) as fh:
                    config = yaml.safe_load(fh, Loader=yaml.FullLoader)
            except Exception as e:
                logger.error(f"Failed to load yaml config from {config}:\n{e}")
                return None

        self.config = config

    def __init__(self, config=dict(), **kwargs):
        self._read_config(config=config)
        self.update_config(**kwargs)
