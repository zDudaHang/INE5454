import json
import os
from typing import Dict, List

from src.constants.paths import *
from src.constants.portal_sp import *

from bs4 import BeautifulSoup, Tag


def extrair_portal_transparencia_sc():
    servidores: List[Dict] = []
    path_to_job1 = os.path.join(RESOURCES_DIR, SC_RESOURCES_DIR, SC_JOB_1)
    for page in range(1, len(os.listdir(path_to_job1)) + 1):
        path_to_page = os.path.join(path_to_job1, str(page) + FILE_EXTENSION)
        with open(path_to_page, 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            colunas = encontrar_colunas(soup)
            servidores = encontrar_valores(colunas, soup, servidores)
    print(servidores)


def encontrar_colunas(soup: BeautifulSoup) -> List[str]:
    colunas: List[str] = []
    thead = soup.find('thead')
    if (isinstance(thead, Tag)):
        ths = thead.find_all('th')
        for th in ths:
            if (isinstance(th, Tag)):
                span = th.find('span')
            if (isinstance(span, Tag)):
                colunas.append(span.text.strip())
    return colunas


def encontrar_valores(colunas: List[str], soup: BeautifulSoup, servidores: List[Dict]) -> List[Dict]:
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        servidor = {}
        for index_th, td in enumerate(tds):
            if (isinstance(td, Tag)):
                span = td.find('span')
                if (isinstance(span, Tag)):
                    servidor[colunas[index_th]] = span.text
        servidores.append(servidor)
    return servidores


if __name__ == '__main__':
    infos_salariais = dict()
    n_entradas = 1
    # TODO: Transformar isso em uma classe para o código ficar mais limpo
    path_to_sp_job1 = os.path.join(RESOURCES_DIR, SP_RESOURCES_DIR, SP_JOB_1)
    # itera pelas paginas salvas em um diretorio qualquer
    for page in range(1, len(os.listdir(path_to_sp_job1)) + 1):
        # abre uma pagina qualquer
        path_to_page = os.path.join(
            path_to_sp_job1, str(page) + FILE_EXTENSION)
        with open(path_to_page, 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            # acha a tag com as informacoes desejadas
            result = soup.find('table', attrs={'rules': 'all'})
            # obtem o elemento de linha de tabela contida na tabela desejada
            trs = result.find_all('tr', attrs=None)
            # itera sobre os elementos linha
            for tr in trs:
                tds = tr.find_all('td')
                # checa se uma linha contem apenas infos de cabecalho; se sim vai para proxima
                if len(tds) < 1:
                    continue
                line = dict()
                # cria um dicionario com as informacoes de uma linha
                for i in range(10):
                    line.update({NOME_CAMPOS[i]: tds[i].text})
                # atualiza o dicionario principal
                infos_salariais.update({n_entradas: line})
                n_entradas = n_entradas + 1

            # apenas imprime o dicionario obtido
            # for i, info in infos_salariais.items():
            #     print(i, '->', info)

    # escreve os dados serializados para um arquivo qualquer
    result_path = os.path.join(
        RESOURCES_DIR, SP_RESOURCES_DIR, RESULT_FOLDER, SP_JOB_1, RESULT_FILENAME)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, 'w') as outfile:
        json.dump(infos_salariais, outfile)

    extrair_portal_transparencia_sc()
