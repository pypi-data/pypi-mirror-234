from ..singleton import Singleton
from ..test_case import DeterministicTestCase
from abc import abstractmethod

#The Singleton metaclass ensures that only one instance of the Metric class is created throughout the program, making it a singleton class
class Metric(metaclass=Singleton):
    # set an arbitrary minimum score that will get over-ridden later
    score: float = 0

    @property
    def minimum_score(self) -> float:
        return self._minimum_score

    @minimum_score.setter
    def minimum_score(self, value: float):
        self._minimum_score = value

    # Measure function signature is subject to be different - not sure
    # how applicable this is - might need a better abstraction --> ??
    @abstractmethod
    def measure(self, test_case: DeterministicTestCase, *args, **kwargs): #non chiaro come si usa
        raise NotImplementedError

    def _get_init_values(self):
        # We use this method for sending useful metadata
        init_values = {
            param: getattr(self, param)
            for param in vars(self)
            if isinstance(getattr(self, param), (str, int, float))
        }
        return init_values

    @abstractmethod
    def is_successful(self) -> bool: #non chiaro come si usa
        raise NotImplementedError

    @property
    def __name__(self):
        return "Metric"