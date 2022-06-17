import os
from termcolor import colored

from src.model.EnvironmentEnum import EnvironmentEnum


def get_bool_env_variable(env_variable_name: str) -> bool:
    variable = os.environ.get(env_variable_name, 'False')
    if variable.casefold() == "true":
        return True
    else:
        return False


def print_when_debug_enabled(text: str) -> None:
    isDebugEnabled = get_bool_env_variable(EnvironmentEnum.DEBUG)
    if isDebugEnabled:
        print(f"[{colored('DEBUG', 'yellow')}] {text}")


def print_when_verbose_enabled(text: str) -> None:
    isVerboseEnabled = get_bool_env_variable(EnvironmentEnum.VERBOSE)
    if isVerboseEnabled:
        print(f"[{colored('VERBOSE', 'cyan')}] {text}")


def print_info_message(text: str) -> None:
    print(f"[{colored('INFO', 'magenta')}] {text}")


def print_success_message(text: str) -> None:
    print(f"[{colored('SUCESSO', 'green')}] {text}")
