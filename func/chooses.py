import random

class Chooses():
    def __init__(self, candidates) -> None:
        self.candidates = candidates

    def apply(self):
        if not isinstance(self.candidates, list) or len(self.candidates) == 0:
            # todo
            return

        candidates_len = len(self.candidates)
        fixed_sz = random.randrange(1, candidates_len)
        if fixed_sz + 1 == candidates_len:
            return self.candidates

        used_idxes = []
        result = []
        for _ in range(0, fixed_sz):
            idx = random.randrange(0, len(self.candidates))
            while idx in used_idxes:
                idx += 1
                idx = idx % len(self.candidates)
            used_idxes.append(idx)
            result.append(self.candidates[idx])
        return result