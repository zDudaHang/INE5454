from abc import ABC, abstractmethod


class Requester(ABC):
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}
    PAGE = ''

    @abstractmethod
    def get_next(self) -> None:
        pass

    @abstractmethod
    def get_html(self) -> None:
        pass

    def get_page(self) -> str:
        self.get_next()
        return self.PAGE

    @abstractmethod
    def has_next(self) -> bool:
        pass
