from optparse import OptionParser
import transformer
from op import Op
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
    transformer.Transformer(options).run()
    
def from_web(op: Op):
    transformer.Transformer(op).run()
    
if __name__ == '__main__':
    main()
