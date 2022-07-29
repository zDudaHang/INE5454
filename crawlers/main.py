import json
import os

from src.constants.paths import *
from src.constants.portal_params_enum import PortalParamsEnum
from src.crawler.PortalSCCrawler import PortalSCCrawler
from src.parser.PortalSEParser import PortalSEParser
from src.parser.PortalSPParser import PortalSPParser
from src.requester.se_requester import SeRequester
from src.requester.sp_requester import SpRequester
from src.util import update_cargos


def get_servidores(portal: str) -> str:
    try:
        enum = PortalParamsEnum[portal]
    except:
        print("Forneca o nome de um orgao suportado: POLICIA_MILITAR, SECRETARIA_SEGURANCA, SECRETARIA_EDUCACAO ou DEPARTAMENTO_TRANSITO")
        exit(1)
    param_sc, param_se, param_sp, dict_atualizacao_cargos = enum.value
    servidores = list()

    sp_requester = SpRequester(orgao=param_sp)
    parser = PortalSPParser()
    servidores.extend(parser.parse_with_requester(sp_requester))

    se_requester = SeRequester(orgao=param_se)
    parser = PortalSEParser()
    servidores.extend(parser.parse_with_requester(se_requester))

    crawler = PortalSCCrawler(
        "http://www.transparencia.sc.gov.br/remuneracao-servidores")
    servidores.extend(crawler.crawl([param_sc]))

    servidores = update_cargos(servidores, dict_atualizacao_cargos)
    return servidores


if __name__ == '__main__':
    servidores = []
    servidores.extend(get_servidores("POLICIA_MILITAR"))
    servidores.extend(get_servidores("SECRETARIA_SEGURANCA"))
    servidores.extend(get_servidores("SECRETARIA_EDUCACAO"))
    servidores.extend(get_servidores("DEPARTAMENTO_TRANSITO"))
    result_path = os.path.join(RESOURCES_DIR, RESULT_FOLDER, RESULT_FILENAME)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, 'w', encoding='utf-8') as outfile:
        json.dump(servidores, outfile, indent=4, ensure_ascii=False)
        print(
            f'[SUCESSO] Os dados processados se encontram no arquivo {result_path}')
