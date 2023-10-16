from .metric import Metric
from ..test_case import DeterministicTestCase
from ..singleton import Singleton


class MinQuestionNumberCheck(Metric, metaclass=Singleton):
    def __init__(self, minimum_score: float = 0.5):
        self.minimum_score = minimum_score
        self.question_per_lengths = 1000

    def measure(self, test_case: DeterministicTestCase):
        self.score = test_case.output / (test_case.input / self.question_per_lengths)
        self.success = self.score >= self.minimum_score
        return self.score

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "MinQuestionNumberCheck"