import os
import getpass
import typing as T
from configparser import ConfigParser
from qtc.ext.enum import Enum
from qtc.ext.logging import set_logger
logger = set_logger()


_DEFAULT_ENV = 'RESEARCH'


class Prop(Enum):
    """Enumeration of vanilla property keys with no special handling."""

    FMS_BASE_URL = 'fms.base_url'


class EnvConfig:
    """
    EnvironmentConfig is a singleton that holds runtim environment configuration (instead of application configuration).
    EnvironmentConfig should be treated as an immutable object.

    EnvironmentConfig should be accessed using the qtc.env_config::get_env_config() method.
    For research, it is sometimes useful to pass environment overrides to get_env_config().

    See additional documentation at qtc.env_config::get_env_config()
    """

    _instance: T.Optional['EnvConfig'] = None
    _env_config_file = None

    @classmethod
    def set_env_config_file(cls, env_config_file):
        EnvConfig._env_config_file = env_config_file

    def __init__(self,
                 environment: str,
                 overrides: T.Dict[str, str],
                 show_splash=False,
                 ) -> None:
        self._environment = environment
        self._overrides = overrides
        self._parser = ConfigParser()

        if self._env_config_file is None:
            self._env_config_file = os.path.join(os.path.dirname(__file__), 'env_config.cfg')
        self._parser.read(self._env_config_file)

        if environment not in self._parser.sections():
            raise Exception(f"Unknown environment '{environment}', "
                            f"expected one of {', '.join(self._parser.sections())}")

        if (environment=='PROD') and overrides:
            raise Exception('overrides are not supported in the PROD environment.')

        user = getpass.getuser()
        # if platform.system() == 'Windows':
        #     # user = os.environ['username']
        #     temp_dir = os.environ['tmp']
        # else:
        #     # user = os.environ['USER']
        #     temp_dir = os.environ.get('TMPDIR', f"/tmp/{user}")
        #
        # # self._options holds values of variables that can be used in the
        # # env_config.cfg file.
        # self._options = dict(user=user,
        #                      temp_dir=temp_dir,
        #                      environment=environment)
        self._options = dict(user=user,
                             environment=environment)

        if show_splash:
            logger.info(75 * '#')
            logger.info(f'###  Initializing EnvConfig with env={environment}, user={user}.')
            for key, val in overrides.items():
                logger.info(f'###     [override]   {key} => {val}')
            logger.info(75 * '#')

    @property
    def environment(self) -> str:
        """
        The short environment string that is explicitly passed in with
        the 'SYSEQUITY_ENV' variable or inferred.
        """
        return self._environment

    def get(self, prop, default: T.Optional[str] = None) -> str:
        """
        Gets the value of a property for this environment. If a value is not available, it will use
        a value associated with the [DEFAULT] section in env_config.cfg.
        """
        if isinstance(prop, str):
            try:
                prop = Prop.retrieve(prop).value
            except:
                pass
        if prop in self._overrides:
            return self._overrides[prop]
        try:
            return self._parser.get(self.environment, prop, vars=self._options)
        except:
            return default

    @staticmethod
    def get_instance(env: T.Optional[str] = None,
                     overrides: T.Optional[T.Dict[str, str]] = None,
                     show_splash=False
                     ) -> 'EnvConfig':
        """
        Gets the Singleton instance of the EnvConfig object. Optionally takes an environment
        and a dictionary of property overrides.

        If a environment is not specified, it will default to the 'SYSEQUITY_ENV' environment variable.

        .. note::
            Normally this method is not called directly, instead, please use
            'qtc.env_config::get_env_config' function.
        """
        if EnvConfig._instance is not None:
            if (env is not None) or overrides:
                raise Exception("Only the first call to 'EnvConfig.get_instance()' can use arguments.")
            return EnvConfig._instance

        if env is None:
            env = os.environ.get('CONNECTION_ENV', _DEFAULT_ENV)

        if env is None:
            raise Exception(f'env={env}: The impossible happened!')

        env = env.upper()
        if overrides is None:
            overrides = dict()

        EnvConfig._instance = EnvConfig(env, overrides, show_splash=show_splash)
        return EnvConfig._instance


def get_env_config(env=None, env_config_file=None, show_splash=False, **overrides):
    if env_config_file is None:
        env_config_file = os.path.join(os.path.dirname(__file__), 'env_config.cfg')
    EnvConfig.set_env_config_file(env_config_file=env_config_file)

    return EnvConfig.get_instance(env=env, overrides=overrides, show_splash=show_splash)