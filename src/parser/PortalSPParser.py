import json
import os

from src.constants.paths import *
from src.constants.html_tags import *
from src.constants.portal_sp import *
from src.parser.Parser import Parser

from bs4 import BeautifulSoup
from bs4.element import Tag


class PortalSPParser(Parser):
    def parse(self):
        infos_salariais = dict()
        n_entradas = 1
        # TODO: Transformar isso em uma classe para o código ficar mais limpo
        path_to_sp_job1 = os.path.join(
            RESOURCES_DIR, SP_RESOURCES_DIR, SP_JOB_1)
        # itera pelas paginas salvas em um diretorio qualquer
        for page in range(1, len(os.listdir(path_to_sp_job1)) + 1):
            # abre uma pagina qualquer
            path_to_page = os.path.join(
                path_to_sp_job1, str(page) + FILE_EXTENSION)
            with open(path_to_page, 'r') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                # acha a tag com as informacoes desejadas
                result = soup.find(TABLE, attrs={'rules': 'all'})
                # obtem o elemento de linha de tabela contida na tabela desejada
                trs = result.find_all(TR, attrs=None)
                # itera sobre os elementos linha
                for tr in trs:
                    tds = tr.find_all(TD)
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
                for i, info in infos_salariais.items():
                    print(i, '->', info)

        # escreve os dados serializados para um arquivo qualquer
        result_path = os.path.join(
            RESOURCES_DIR, SP_RESOURCES_DIR, RESULT_FOLDER, SP_JOB_1, RESULT_FILENAME)
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        with open(result_path, 'w') as outfile:
            json.dump(infos_salariais, outfile)

    def validate(self):
        pass
