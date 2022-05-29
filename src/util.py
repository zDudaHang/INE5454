import os

from src.model.EnvironmentEnum import EnvironmentEnum
from src.constants.paths import HTML_EXTENSION


def get_bool_env_variable(env_variable_name: str) -> bool:
    variable = os.environ.get(env_variable_name, False)
    if variable.casefold() == "true":
        return True
    else:
        return False


def print_when_debug_enabled(text: str) -> None:
    isDebugEnabled = get_bool_env_variable(EnvironmentEnum.DEBUG)
    if isDebugEnabled:
        print(f'[DEBUG] {text}')


def print_when_verbose_enabled(text: str) -> None:
    isVerboseEnabled = get_bool_env_variable(EnvironmentEnum.VERBOSE)
    if isVerboseEnabled:
        print(f'[DEBUG] {text}')


def get_file_extension(filePath: str) -> str:
    _, fileExtension = os.path.splitext(filePath)
    return fileExtension


def is_html_file(filePath: str) -> bool:
    return get_file_extension(filePath) == HTML_EXTENSION
