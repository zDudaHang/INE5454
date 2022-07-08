from abc import ABC, abstractmethod


class Requester(ABC):
    URL: str = ''
    HEADERS: dict = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
    PAGE: str = ''
    VIEWSTATE: str = ''
    STARTED: bool = False

    @abstractmethod
    def get_next(self):
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
