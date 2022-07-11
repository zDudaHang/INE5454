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
from src.parser.PortalSEParser import PortalSEParser
from src.requester.se_requester import SeRequester

from src.util import print_when_debug_enabled

if __name__ == '__main__':
    load_dotenv('/home/duda/INE5454/.env')

    se_requester = SeRequester()
    parser = PortalSEParser('')
    result = parser.parse_with_requester(se_requester)
    print('bk')
    # while se_requester.has_next():
    #     print(se_requester.get_next())
