import decimal
import os
import configparser

_config = configparser.ConfigParser()
_config.read("config.ini", encoding="utf-8")


def _get_from_config_or_env(section: str, key: str) -> str:
    result = _config[section].get(key)
    if not result:
        result = os.environ[f"{section}:{key}"]
    return result


DEBUG = bool(int(_get_from_config_or_env("default", "debug")))
RUNNING_MODULES = _get_from_config_or_env("default", "running_modules").split()

ALEMBIC_SA_URL = _get_from_config_or_env("db", "alembic_sa_url")

SA_URL = _get_from_config_or_env("db", "sa_url")
SA_ECHO = bool(int(_get_from_config_or_env("db", "sa_echo")))
NAME_TABLE = _get_from_config_or_env("db", "table")

URL = _get_from_config_or_env("api", "url")
API_KEY = _get_from_config_or_env("api", "api_key")