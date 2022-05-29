from src.constants.paths import *
from src.constants.portal_sp import *
from src.constants.html_tags import *

from src.parser.PortalSCParser import PortalSCParser
from src.parser.PortalSPParser import PortalSPParser

if __name__ == '__main__':
    scParser = PortalSCParser()
    spParser = PortalSPParser()

    scParser.parse()
    spParser.parse()
