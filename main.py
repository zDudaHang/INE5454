import json
import os
from src.constants.paths import *
from src.constants.portal_sp import *
from src.constants.html_tags import *

from src.parser.PortalSCParser import PortalSCParser
from src.parser.PortalSPParser import PortalSPParser

if __name__ == '__main__':
    scParser = PortalSCParser()
    spParser = PortalSPParser()

    servidoresSC = scParser.parse()
    servidoresSP = spParser.parse()

    servidores = servidoresSC + servidoresSP

    result_path = os.path.join(
        RESOURCES_DIR, RESULT_FOLDER, RESULT_FILENAME)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, 'w', encoding='utf-8') as outfile:
        json.dump(servidores, outfile, indent=4, ensure_ascii=False)
