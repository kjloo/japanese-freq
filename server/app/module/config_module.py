import os
from app.module.config.anki_config import AnkiConfig
import yaml
import importlib.resources as pkg_resources


def _load_yaml_config(env: str) -> dict:
    """
    Load configuration from a YAML file based on the environment.
    :param env: The environment name (e.g., 'development', 'testing', 'production').
    :return: A dictionary with the configuration data.
    """
    file_name = f"config-{env}.yaml"
    default_file_name = "config.yaml"

    try:
        with pkg_resources.files('app.resources').joinpath(file_name).open('r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        try:
            with pkg_resources.files('app.resources').joinpath(default_file_name).open('r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Neither environment-specific nor default configuration file found.")


def _get_env() -> str:
    """
    Get the current environment from the environment variable.
    :return: The environment name (e.g., 'development', 'testing', 'production').
    """
    env = os.getenv("ENV", "local")
    if env not in ["local", "development", "testing", "production"]:
        raise ValueError("Invalid environment specified.")
    return env


env = _get_env()
config = _load_yaml_config(env)


class BaseConfig(object):
    """
    Base configuration with default settings.
    """
    DEBUG = False
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_SORT_KEYS = False

    LOG_LEVEL = "INFO"
    ANKI_SERVER_URL = AnkiConfig(config).get_server_url()


class LocalConfig(BaseConfig):
    """
    Local-specific configuration.
    """
    DEBUG = True

    LOG_LEVEL = "DEBUG"


class DevelopmentConfig(BaseConfig):
    """
    Development-specific configuration.
    """
    DEBUG = False


class TestingConfig(BaseConfig):
    """
    Testing-specific configuration.
    """
    TESTING = True


class ProductionConfig(BaseConfig):
    """
    Production-specific configuration.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "production-secret-key")


# Configuration mapping for different environments
config_map = {
    "local": LocalConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

config = config_map.get(env, LocalConfig)
