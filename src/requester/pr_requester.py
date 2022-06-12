import requests

from src.requester.requester import Requester


class PrRequester(Requester):
    def __init__(self):
        self.page = ''

    def get_html(self) -> None:
        params = dict()
        r = requests.get(self.URL, params=params)
        pass

    def get_page(self) -> str:
        pass

    def has_next(self) -> bool:
        pass

    def get_next(self) -> None:
        pass
