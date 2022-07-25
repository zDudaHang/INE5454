import json

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

    crawler = PortalSCCrawler("http://www.transparencia.sc.gov.br/remuneracao-servidores")
    servidores.extend(crawler.crawl([param_sc]))

    servidores = update_cargos(servidores, dict_atualizacao_cargos)
    return json.dumps({'servidores': servidores})


if __name__ == '__main__':
    print(get_servidores("POLICIA_MILITAR"))
    print(get_servidores("SECRETARIA_SEGURANCA"))
    print(get_servidores("SECRETARIA_EDUCACAO"))
    print(get_servidores("DEPARTAMENTO_TRANSITO"))
    print('todos extraidos com sucesso')
