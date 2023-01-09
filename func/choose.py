import random


class Choose():
    def __init__(self, candidates) -> None:
        self.candidates = candidates

    def apply(self):
        if not isinstance(self.candidates, list) or len(self.candidates) == 0:
            return
        idx = random.randrange(0, len(self.candidates))
        return self.candidates[idx]
