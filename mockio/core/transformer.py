from mockio.extensions import common_function_dict, placeholder
from box import Box
import copy
from tqdm import tqdm
from mockio.core.op import Op
from typing import List

class Transformer():
    DEFAULT_SIZE = 1000
    def __init__(self, op: Op) -> None:
        self.op = op
        
    @staticmethod
    def RUN(op: Op) -> List[str]:
        return Transformer(op).run()
        
    def parse(self, values: dict):
        result = {}
        self.transform(values, result)
        return result
        
    def transform(self, values, result: dict, real_name: str='', dot_name: str='',):
        if real_name in common_function_dict.keys():
            result[dot_name] = common_function_dict[real_name](values)
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
        return self.DEFAULT_SIZE
        
    def run(self) -> List[str]:
        records : List[str] = list() 
        for collection, values in self.op.template.items():
            self.for_collection(collection, values)
            print_info = f'Import {self.op.num} documents into {collection}'
            records.append(print_info)
            print(print_info)        
        return records
    def for_collection(self, collection: str, values: dict):
        with tqdm(total=self.op.num) as pbar:
            round_result = []
            for i in range(0, self.op.num):
                vals = copy.deepcopy(values)
                result = self.parse(vals)
                boxed_vals = Box(vals)
                for k, func in result.items():
                    # Apply the placeholder function and set the value using attribute access
                    keys = k.split('.')
                    current = boxed_vals
                    for key in keys[:-1]:
                        current = getattr(current, key)
                    setattr(current, keys[-1], func.apply())
                round_result.append(boxed_vals.to_dict())
                if i + 1 == self.op.num or (i + 1) % self.get_batch_number() == 0:
                    batch_size = len(round_result)
                    self.op.client.bulk_insert(collection, round_result)
                    pbar.update(batch_size)
                    round_result.clear()