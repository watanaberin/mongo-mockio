from optparse import OptionParser
import json
from func import choose, chooses, between, placeholder
from box import Box
import copy

DEFUALT_SIZE = 1000

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
    (options, args) = parser.parse_args()
    
    with open(options.filepath, 'r') as f:
        template = json.load(f)
    
    for collection, values in template.items():
        for i in range(0, options.num):
            vals = copy.deepcopy(values)
            result = parse(vals)
            boxed_vals = Box(vals)
            if i != 0 and i %options.num == 0:
                pass
            for k, func in result.items():
                exec(f'boxed_vals.{k} = func.apply()') 
if __name__ == '__main__':
    main()
