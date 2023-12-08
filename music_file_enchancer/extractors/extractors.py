from abc import ABC, abstractmethod


class NotFoundError(Exception):
    pass


class Extractor_interface(ABC):
    @abstractmethod
    def data_json(self):
        pass
