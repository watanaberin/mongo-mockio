import random
from datetime import datetime

def trans_to_date(date) -> datetime:
        try:
            if ':' in date:
                t = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            else:
                t = datetime.strptime(date, '%Y-%m-%d')
            return t
        except:
            return datetime.now() 
class Between():
    def __init__(self, candidates) -> None:
        self.candidates = candidates

    def apply(self):
        if not isinstance(self.candidates, list) or len(self.candidates) < 2:
            return
        fisrt = self.candidates[0]
        second = self.candidates[1]
        if isinstance(fisrt, int) and isinstance(second, int):
            return random.choice(self.candidates[:2])
        if isinstance(fisrt, str) and isinstance(second, str):
            first_time = trans_to_date(fisrt)
            second_time = trans_to_date(second)
            if first_time and second_time:
                f = int(first_time.timestamp())
                s = int(second_time.timestamp())
                ts = random.randrange(f,s)
                datetime.fromtimestamp(ts)
                return datetime.fromtimestamp(ts)
