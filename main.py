import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from src.constants.paths import *
from src.constants.portal_sp import *
from src.constants.html_tags import *

from src.crawler.PortalSCCrawler import PortalSCCrawler

from src.util import print_info_message, print_when_debug_enabled

URL_PORTAL_SC = "http://www.transparencia.sc.gov.br/remuneracao-servidores"

if __name__ == '__main__':
    load_dotenv('/home/bridge/INE5454/.env')

    crawler = PortalSCCrawler(URL_PORTAL_SC)
    servidores = crawler.crawl()
    # print(servidores)

    # spParser = PortalSPParser(os.path.join(RESOURCES_DIR, SP_RESOURCES_DIR))

    # servidoresSC = scParser.parse_resources()
    # servidoresSP = spParser.parse_resources()

    # servidores = servidoresSC + servidoresSP

    # print_when_debug_enabled(
    #     f'Quantidade de servidores encontrados: {servidores.__len__()}')

    # result_path = os.path.join(
    #     RESOURCES_DIR, RESULT_FOLDER, RESULT_FILENAME)
    # os.makedirs(os.path.dirname(result_path), exist_ok=True)
    # with open(result_path, 'w', encoding='utf-8') as outfile:
    #     json.dump(servidores, outfile, indent=4, ensure_ascii=False)
    #     print(
    #         f'[SUCESSO] Os dados processados se encontram no arquivo {result_path}')
