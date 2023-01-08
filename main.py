import random
from optparse import OptionParser

class Choose():
    def __init__(self, be_choosed) -> None:
        self.be_choosed = be_choosed

    def choose_action(self):
        if not isinstance(self.be_choosed, list) or len(self.be_choosed) == 0:
            return
        idx = random.randrange(0, len(self.be_choosed))
        return self.be_choosed[idx]


class Chooses():
    def __init__(self, be_choosed) -> None:
        self.be_choosed = be_choosed

    def choose_action(self):
        if not isinstance(self.be_choosed, list) or len(self.be_choosed) == 0:
            # todo 
            return
        
        choosed_len = len(self.be_choosed)
        fixed_sz = random.randrange(1, choosed_len)
        if fixed_sz + 1 == choosed_len:
            return self.be_choosed
    
        used_idxes = []
        result = []
        for _ in range(0, fixed_sz):
            idx = random.randint(0, len(self.be_choosed))
            while idx in used_idxes:
                idx+=1
                idx = idx % len(self.be_choosed)
            used_idxes.append(idx)
            result.append(self.be_choosed[idx])
        return result

common_function_dict = {
    '$choose': Choose,
    '$chooses': Chooses,    
}

def main():
    pass

if __name__ == '__main__':
    main()