from optparse import OptionParser
import json
from func import choose, chooses, between, placeholder
from box import Box
from myclient import MyClient
import copy
from tqdm import tqdm
import time

DEFUALT_SIZE = 100

common_function_dict = {
    '$choose': choose.Choose,
    '$chooses': chooses.Chooses,
    '$between': between.Between,
}

def parse(values: dict):
    result = {}
    transform(values, result)
    return result
    
def transform(values, result: dict, real_name: str='', dot_name: str='',):
    if real_name in common_function_dict.keys():
        result[dot_name] = common_function_dict[real_name](values)
    elif isinstance(values, str) and values.startswith('$'):
        result[dot_name] = placeholder.Placeholder(values)
    if isinstance(values, dict):
        for name, inner_vals in values.items():
            transform(inner_vals, result, name, add_last_with_dot_format(dot_name, name))
    
def add_last_with_dot_format(full: str, last: str) -> str:
    if full.strip() == '':
        return last
    if last.startswith('$'):
        return full
    return f'{full}.{last}'
           
def main():
    parser = OptionParser()
    parser.add_option('-f', '--filepath', dest='filepath',
                      help='template json file path')
    parser.add_option('-n', '--num', dest='num', type='int',
                      help='how many datas need mock')
    parser.add_option('-m', '--host', dest='host', type='str',
                      help='mongo host,localhost:27017')
    parser.add_option('-d', '--db', dest='db', type='str',
                    help='target db name')
    (options, args) = parser.parse_args()
    
    with open(options.filepath, 'r') as f:
        template = json.load(f)
    client = MyClient(options.host, options.db)
    for collection, values in template.items():
        with tqdm(total=options.num) as pbar:
            round_result = []
            for i in range(0, options.num):
                vals = copy.deepcopy(values)
                result = parse(vals)
                boxed_vals = Box(vals)
                for k, func in result.items():
                    exec(f'boxed_vals.{k} = func.apply()')   
                round_result.append(boxed_vals.to_dict())
                if i + 1 == options.num or (i + 1) % DEFUALT_SIZE == 0:
                    client.bulk_insert(collection, round_result)
                    pbar.update(i+1)
                    round_result = []
                    

if __name__ == '__main__':
    main()
