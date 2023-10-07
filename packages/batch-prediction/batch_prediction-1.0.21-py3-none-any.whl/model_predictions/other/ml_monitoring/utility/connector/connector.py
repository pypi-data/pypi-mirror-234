import abc
from typing import Tuple
from pandas import DataFrame

class Connector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_data(self) -> Tuple[DataFrame,DataFrame]:
        pass
