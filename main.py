from dotenv import load_dotenv

from src.constants.paths import *
from src.constants.portal_sp import *
from src.constants.html_tags import *

from src.crawler.PortalSCCrawler import PortalSCCrawler
from src.parser.PortalSEParser import PortalSEParser
from src.parser.PortalSPParser import PortalSPParser
from src.requester.se_requester import SeRequester
from src.requester.sp_requester import SpRequester

URL_PORTAL_SC = "http://www.transparencia.sc.gov.br/remuneracao-servidores"

if __name__ == '__main__':
    # load_dotenv('/home/bridge/INE5454/.env')


    sp_requester = SpRequester(orgao=71)
    parser = PortalSPParser()
    results = parser.parse_with_requester(sp_requester)

    se_requester = SeRequester(orgao=4)
    parser = PortalSEParser()
    results.extend(parser.parse_with_requester(se_requester))

    crawler = PortalSCCrawler(URL_PORTAL_SC)
    results.extend(crawler.crawl(['DESESA CIVIL']))
    for result in results:
        print(result)
