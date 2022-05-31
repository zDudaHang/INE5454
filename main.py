from ast import List
import json
import os
from typing import Dict
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import json

from src.constants.paths import *
from src.constants.portal_sp import *
from src.constants.html_tags import *

from src.parser.PortalSCParser import PortalSCParser
from src.parser.PortalSPParser import PortalSPParser
from src.parser.PortalMGParser import PortalMGParser
from src.parser.PortalPRParser import PortalPRParser

from src.util import print_when_debug_enabled

if __name__ == '__main__':
    load_dotenv('/home/duda/INE5454/.env')

    scParser = PortalSCParser(os.path.join(RESOURCES_DIR, SC_RESOURCES_DIR))
    spParser = PortalSPParser(os.path.join(RESOURCES_DIR, SP_RESOURCES_DIR))
    mgParser = PortalMGParser(os.path.join(RESOURCES_DIR, MG_RESOURCES_DIR))
    prParser = PortalPRParser(os.path.join(RESOURCES_DIR, PR_RESOURCES_DIR))

    servidoresSC = scParser.parse_resources()
    servidoresSP = spParser.parse_resources()
    servidoresMG = mgParser.parse_resources()
    servidoresPR = prParser.parse_resources()

    servidores = servidoresSC + servidoresSP + servidoresMG + servidoresPR

    print_when_debug_enabled(
        f'Quantidade de registros encontrados: {servidores.__len__()}')

    result_path = os.path.join(
        RESOURCES_DIR, RESULT_FOLDER, RESULT_FILENAME)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, 'w', encoding='utf-8') as outfile:
        json.dump(servidores, outfile, indent=4, ensure_ascii=False)
        print(
            f'[SUCESSO] Os dados processados se encontram no arquivo {result_path}')

    # list = json.load(open(result_path, 'r'))
    # print(list[0])
    # xAxis = [value[PORTAL_DICT_KEY] for value in list]
    # yAxis = [0 for value in list]
    # plt.grid(True)

    # ## LINE GRAPH ##
    # plt.plot(xAxis, yAxis, color='maroon', marker='o')
    # plt.xlabel('variable')
    # plt.ylabel('value')

    # plt.show()
