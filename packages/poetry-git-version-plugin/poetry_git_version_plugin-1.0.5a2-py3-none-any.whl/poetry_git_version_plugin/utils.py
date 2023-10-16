from typing import Any

from poetry_git_version_plugin.exceptions import (
    InvalidCanonPepVersionException,
    InvalidPepVersionException,
    InvalidVersionException,
)
from poetry_git_version_plugin.regex_compiles import (
    VERSION_PEP440_CANON_REGEX_COMPILE,
    VERSION_PEP440_REGEX_COMPILE,
    VERSION_UNIVERSAL_REGEX,
)

TRUE_VALUES = {'y', 'yes', 't', 'true', 'on', '1', '+'}
FALSE_VALUES = {'n', 'no', 'f', 'false', 'off', '0', '-', ''}


def serialize_to_boolean(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value

    value = str(value).lower()

    if value in TRUE_VALUES:
        return True

    if value in FALSE_VALUES:
        return False

    return default


def validate_version(version_string: str):
    """Проверка версии на PEP 440 и общепринятой семантики

    Args:
        version_string (str): Версия

    Raises:
        PluginException: Версия не соответствует стандарту

    """

    if VERSION_PEP440_REGEX_COMPILE.search(version_string) is None:
        raise InvalidPepVersionException(version_string)

    if VERSION_PEP440_CANON_REGEX_COMPILE.search(version_string) is None:
        raise InvalidCanonPepVersionException(version_string)

    if VERSION_UNIVERSAL_REGEX.search(version_string) is None:
        raise InvalidVersionException(version_string)
