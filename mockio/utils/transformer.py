from mockio.func import choose, chooses, between, placeholder
from box import Box
import copy
from tqdm import tqdm
from mockio.utils.op import Op


class Transformer():
    common_function_dict = {
    '$choose': choose.Choose,
    '$chooses': chooses.Chooses,
    '$between': between.Between,
    }
    DEFUALT_SIZE = 1000
    def __init__(self, op: Op) -> None:
        self.op = op
        
    @staticmethod
    def RUN(op: Op):
        Transformer(op).run()
        
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
        return self.DEFUALT_SIZE
        
    def run(self):
        for collection, values in self.op.template.items():
            self.for_collection(collection, values)
                        
    def for_collection(self, collection: str, values: dict):
        with tqdm(total=self.op.num) as pbar:
            round_result = []
            for i in range(0, self.op.num):
                vals = copy.deepcopy(values)
                result = self.parse(vals)
                boxed_vals = Box(vals)
                for k, func in result.items():
                    exec(f'boxed_vals.{k} = func.apply()')
                round_result.append(boxed_vals.to_dict())
                if i + 1 == self.op.num or (i + 1) % self.get_batch_number() == 0:
                    self.op.client.bulk_insert(collection, round_result)
                    pbar.update(i+1)
                    round_result.clear()