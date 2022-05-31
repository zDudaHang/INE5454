import os
import re
from src.model.EnvironmentEnum import EnvironmentEnum
from src.constants.paths import HTML_EXTENSION

UNWANTED_SYMBOLS = ['R$ ']


def get_bool_env_variable(env_variable_name: str) -> bool:
    variable = os.environ.get(env_variable_name, False)
    if variable.casefold() == "true":
        return True
    else:
        return False


def clean_text(text: str) -> str:
    text_without_unwanted_symbols = text.strip()
    for symbol in UNWANTED_SYMBOLS:
        text_without_unwanted_symbols = text_without_unwanted_symbols.replace(
            symbol, '')
    text_without_control_chars = text_without_unwanted_symbols.replace(
        '\n', '').replace('\t', '')
    return re.sub('\s{2,}', ' ', text_without_control_chars)


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
