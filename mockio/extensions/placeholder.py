import random
from datetime import datetime
import json
import os
from faker import Faker
from typing import Any
features = [
    '$ip',
    '$incrementIntId',
    '$faker',
]
FIXED_RANDOM_RANGE = 20

class Placeholder:
    _cache = []

    def __init__(self, ph: str, multi=False) -> None:
        self._ph = ph
        self._multi = multi
        self.faker = Faker()
        if self._get_placeholder() not in features or self.is_sub_placeholder(self._get_placeholder()):
            self._get_from_source()

    def is_sub_placeholder(self, s: str):
        if s.startswith('$faker.'):
            return True

    def apply(self):
        if self._get_placeholder() == '$ip':
            return self._get_ip()
        elif self._get_placeholder() == '$incrementIntId':
            return self.gen_increment_id()
        elif self._get_placeholder().startswith('$faker.'):
            return self.gen_faker_lib()
        elif len(self._cache) > 0:
            return self.load_from_source()
            
    def load_from_source(self):
        cache_len = len(self._cache)
        if self._multi:
            cap = FIXED_RANDOM_RANGE if cache_len > FIXED_RANDOM_RANGE else cache_len
            cnt = random.randrange(0, cap)
            res = set()
            for _ in range(0, cnt):
                res_idx = random.randrange(0, cache_len)
                res.add(self._cache[res_idx])
            return list(res)
        else:
            idx = random.randrange(0, cache_len)
            return self._cache[idx]

    def gen_increment_id(self) -> int:
        if len(self._cache) == 0:
            self._cache.append(1)
            return 1
        else:
            self._cache[0] += 1
            return self._cache[0]

    def gen_faker_lib(self) -> Any:
        sub_name: str = self._get_placeholder().split('.')[-1]
        faker_method = getattr(self.faker, sub_name, None)
        if faker_method and callable(faker_method):
            return faker_method()
        return None
        
    def _get_filename(self):
        if self._ph.startswith('$'):
            return self._ph[1:]
        return self._ph

    def _get_placeholder(self) -> str:
        if not self._ph.startswith('$'):
            return '$' + self._ph
        return self._ph

    def _get_ip(self):
        if not self._multi:
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
            # Get the directory where mockio package is located
            package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            source_path = os.path.join(package_dir, 'source', f'{filename}.json')
            with open(source_path, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return

