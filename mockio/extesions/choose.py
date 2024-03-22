import random
from .placeholder import Placeholder

class Choose():
    def __init__(self, candidates) -> None:
        if isinstance(candidates, list):
            self.candidates = candidates
        elif isinstance(candidates, str):
            self.candidates = Placeholder(candidates)

    def apply(self):
        if isinstance(self.candidates, list):
            idx = random.randrange(0, len(self.candidates))
            return self.candidates[idx]
        elif isinstance(self.candidates, Placeholder):
            return self.candidates.apply()
