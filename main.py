from src.constants.portal_params_enum import PortalParamsEnum
from src.crawler.PortalSCCrawler import PortalSCCrawler
from src.parser.PortalSEParser import PortalSEParser
from src.parser.PortalSPParser import PortalSPParser
from src.requester.se_requester import SeRequester
from src.requester.sp_requester import SpRequester

URL_PORTAL_SC = "http://www.transparencia.sc.gov.br/remuneracao-servidores"


def get_cargos(servidores: list[dict]) -> list:
    cargos = list()
    for servidor in servidores:
        if servidor['CARGO'] not in cargos:
            cargos.append(servidor['CARGO'])
    return cargos


def write_to_file(cargos: list, filename: str) -> None:
    with open(f'{filename}', 'w') as fp:
        for cargo in cargos:
            fp.write("%s\n" % cargo)
        print('Done')


if __name__ == '__main__':
    # load_dotenv('/home/bridge/INE5454/.env')
    for params in PortalParamsEnum:
        param_sc, param_se, param_sp = params.value
        results = list()
        #
        # sp_requester = SpRequester(orgao=param_sp)
        # parser = PortalSPParser()
        # results.extend(parser.parse_with_requester(sp_requester))
        #
        # se_requester = SeRequester(orgao=param_se)
        # parser = PortalSEParser()
        # results.extend(parser.parse_with_requester(se_requester))

        crawler = PortalSCCrawler(URL_PORTAL_SC)
        results.extend(crawler.crawl([param_sc]))
        write_to_file(get_cargos(servidores=results), f'{params.name}_values_sc.txt')
