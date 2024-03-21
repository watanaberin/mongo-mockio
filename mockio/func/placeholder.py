import random
from datetime import datetime
import json

features = [
    '$ip'
]
FIXED_RAMDOM_RANGE = 20

class Placeholder:
    _cache = []

    def __init__(self, ph: str, multi=False) -> None:
        self._ph = ph
        self._muilt = multi
        
        if self._get_placeholder() not in features:
            self._get_from_source()

    def apply(self):
        if self._get_placeholder() == '$ip':
            return self._get_ip()
        elif len(self._cache) > 0:
            cache_len = len(self._cache)
            if self._muilt:
                cap = FIXED_RAMDOM_RANGE if cache_len > FIXED_RAMDOM_RANGE else cache_len
                cnt = random.randrange(0, cap)
                res = set()
                for _ in range(0, cnt):
                    res_idx = random.randrange(0, cache_len)
                    res.add(self._cache[res_idx])
                return list(res)
            else:
                idx = random.randrange(0, cache_len)
                return self._cache[idx]

    def _get_filename(self):
        if self._ph.startswith('$'):
            return self._ph[1:]
        return self._ph

    def _get_placeholder(self):
        if not self._ph.startswith('$'):
            return '$' + self._ph
        return self._ph

    def _get_ip(self):
        if not self._muilt:
            return self._generate_ip()
        total = random.randint(1, 20)
        ips = []
        for _ in range(0, total):
            ips.append(self._generate_ip())
        return ips
    
    def _generate_ip(self):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        d = random.randint(0, 255)
        return f'{a}.{b}.{c}.{d}'
    
    def _get_from_source(self):
        filename = self._get_filename()
        try:
            with open(f'source/{filename}.json', 'r') as f:
                self._cache = json.load(f)
        except:
            return

