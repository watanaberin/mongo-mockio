from optparse import OptionParser
import mockio.utils.transformer as transformer
from .utils.op import Op
from .utils.myclient import mclient
import json
def init_option():
    parser = OptionParser()
    parser.add_option('-f', '--filepath', dest='filepath',
                      help='template json file path')
    parser.add_option('-n', '--num', dest='num', type='int',
                      help='how many datas need mock')
    parser.add_option('-b', '--BatchNumber', dest='batch_num', type='int',
                      help='number of bulk insert')
    parser.add_option('-m', '--host', dest='host', type='str',
                      help='mongo host,localhost:27017')
    parser.add_option('-d', '--db', dest='db', type='str',
                    help='target db name')       
    return parser.parse_args()

def main():
    (options, args) = init_option()
    with open(options.filepath, 'r') as f:
        template = json.load(f)
    client = mclient(options.host, options.db)
    num = options.num
    op: Op = Op(template, client, num)
    transformer.Transformer(op).run()
        
if __name__ == '__main__':
    main()
