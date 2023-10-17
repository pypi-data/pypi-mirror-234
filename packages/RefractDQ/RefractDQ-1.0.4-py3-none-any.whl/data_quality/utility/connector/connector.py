import abc
from pandas import DataFrame

class Connector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_data(self) -> DataFrame:
        pass
