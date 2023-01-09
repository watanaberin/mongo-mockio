import random


class Between():
    def __init__(self, candidates) -> None:
        self.candidates = candidates

    def apply(self):
        if not isinstance(self.candidates, list) or len(self.candidates) < 2:
            return
        fisrt = self.candidates[0]
        second = self.candidates[1]
        idx = random.randrange(fisrt, second)
        return idx
