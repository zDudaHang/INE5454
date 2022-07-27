import os
from termcolor import colored
from typing import List

from src.model.EnvironmentEnum import EnvironmentEnum


def get_bool_env_variable(env_variable_name: str) -> bool:
    variable = os.environ.get(env_variable_name, 'False')
    if variable.casefold() == "true":
        return True
    else:
        return False


def convert_BR_number_to_EN_number(text: str) -> str:
    text_without_period = text.replace('.', '')
    return text_without_period.replace(',', '.')


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


def print_error_message(text: str) -> None:
    print(f"[{colored('ERRO', 'red')}] {text}")


def get_cargos(servidores: List[dict]) -> list:
    cargos = list()
    for servidor in servidores:
        if servidor['CARGO'] not in cargos:
            cargos.append(servidor['CARGO'])
    return cargos


def write_to_file(cargos: list, filename: str) -> None:
    with open(f'{filename}', 'w') as fp:
        fp.write('{')
        for cargo in cargos:
            fp.write('"%s": "",\n' % cargo)
        fp.write('}')
        print('Done')


def update_cargos(servidores: List[dict], cargos_atualizados: dict) -> List[dict]:
    for servidor in servidores:
        if servidor['CARGO'] in cargos_atualizados.keys():
            servidor['CARGO'] = cargos_atualizados[servidor['CARGO']]
    return servidores
