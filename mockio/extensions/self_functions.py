from abc import ABC, abstractmethod
from datetime import datetime
import random
from .placeholder import Placeholder

__all__ = ['get_sub_cls_mapping', 'AbstractFunction']
def get_sub_cls_mapping(cls) -> dict:
        all_subclasses = {}

        for subclass in cls.__subclasses__():
            all_subclasses[subclass.name()] = subclass

        return all_subclasses
    
class AbstractFunction(ABC):
    
    @staticmethod
    @abstractmethod
    def name():
        pass
    
    @abstractmethod
    def apply(self):
        pass
    
def trans_to_date(date) -> datetime:
        try:
            if ':' in date:
                t = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            else:
                t = datetime.strptime(date, '%Y-%m-%d')
            return t
        except:
            return datetime.now() 
class Between(AbstractFunction):
    def __init__(self, candidates) -> None:
        self.candidates = candidates
    
    def name():
        return "$between"
    
    def apply(self):
        if not isinstance(self.candidates, list) or len(self.candidates) < 2:
            return
        first = self.candidates[0]
        second = self.candidates[1]
        if isinstance(first, int) and isinstance(second, int):
            return random.randint(first, second)
        if isinstance(first, str) and isinstance(second, str):
            first_time = trans_to_date(first)
            second_time = trans_to_date(second)
            if first_time and second_time:
                f = int(first_time.timestamp())
                s = int(second_time.timestamp())
                ts = random.randrange(f, s)
                return datetime.fromtimestamp(ts)

class Choose(AbstractFunction):
    def __init__(self, candidates) -> None:
        if isinstance(candidates, list):
            self.candidates = candidates
        elif isinstance(candidates, str):
            self.candidates = Placeholder(candidates)
    
    def name():
        return "$choose"
    
    def apply(self):
        if isinstance(self.candidates, list):
            idx = random.randrange(0, len(self.candidates))
            return self.candidates[idx]
        elif isinstance(self.candidates, Placeholder):
            return self.candidates.apply()

class Chooses(AbstractFunction):
    def __init__(self, candidates) -> None:
        if isinstance(candidates, list):
            self.candidates = candidates
        elif isinstance(candidates, str):
            self.candidates = Placeholder(candidates, True)

    def name():
        return "$chooses"
    
    def apply(self):        
        if isinstance(self.candidates, list):
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
        elif isinstance(self.candidates, Placeholder):
            return self.candidates.apply()
        
        
