from .metric import Metric
from ..test_case import DeterministicTestCase
from ..singleton import Singleton


class MaxQuestionNumberCheck(Metric, metaclass=Singleton):
    def __init__(self, maximum_score: float = 1.5):
        self.maximum_score = maximum_score
        self.question_per_lengths = 1000

    def measure(self, test_case: DeterministicTestCase):
        self.score = test_case.output / (test_case.input / self.question_per_lengths)
        self.success = self.score <= self.maximum_score
        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "MaxQuestionNumberCheck"