from func import choose, chooses, between, placeholder
import json
from myclient import MyClient
from box import Box
from myclient import MyClient
import copy
from tqdm import tqdm

class Transformer():
    common_function_dict = {
    '$choose': choose.Choose,
    '$chooses': chooses.Chooses,
    '$between': between.Between,
    }
    DEFUALT_SIZE = 1000
    def __init__(self, options) -> None:
        self.options = options
    def parse(self, values: dict):
        result = {}
        self.transform(values, result)
        return result
        
    def transform(self, values, result: dict, real_name: str='', dot_name: str='',):
        if real_name in self.common_function_dict.keys():
            result[dot_name] = self.common_function_dict[real_name](values)
        elif isinstance(values, str) and values.startswith('$'):
            result[dot_name] = placeholder.Placeholder(values)
        if isinstance(values, dict):
            for name, inner_vals in values.items():
                self.transform(inner_vals, result, name, self.add_last_with_dot_format(dot_name, name))
        
    def add_last_with_dot_format(self, full: str, last: str) -> str:
        if full.strip() == '':
            return last
        if last.startswith('$'):
            return full
        return f'{full}.{last}'
    
    def get_batch_number(self):
        if not self.options.batch_num:
            return self.DEFUALT_SIZE
        return self.options.batch_num
    
    def run(self):
        with open(self.options.filepath, 'r') as f:
            template = json.load(f)
        client = MyClient(self.options.host, self.options.db)
        for collection, values in template.items():
            print(f'Begin to generate {collection}')
            with tqdm(total=self.options.num) as pbar:
                round_result = []
                for i in range(0, self.options.num):
                    vals = copy.deepcopy(values)
                    result = self.parse(vals)
                    boxed_vals = Box(vals)
                    for k, func in result.items():
                        exec(f'boxed_vals.{k} = func.apply()')
                    round_result.append(boxed_vals.to_dict())
                    if i + 1 == self.options.num or (i + 1) % self.get_batch_number() == 0:
                        client.bulk_insert(collection, round_result)
                        pbar.update(i+1)
                        round_result.clear()