from abc import ABC, abstractmethod


class Requester(ABC):

    @abstractmethod
    def get_next(self) -> None:
        pass

    @abstractmethod
    def get_html(self) -> None:
        pass

    @abstractmethod
    def get_page(self) -> str:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass
