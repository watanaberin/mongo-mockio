from optparse import OptionParser
import transformer

def init_option():
    parser = OptionParser()
    parser.add_option('-f', '--filepath', dest='filepath',
                      help='template json file path')
    parser.add_option('-n', '--num', dest='num', type='int',
                      help='how many datas need mock')
    parser.add_option('-m', '--host', dest='host', type='str',
                      help='mongo host,localhost:27017')
    parser.add_option('-d', '--db', dest='db', type='str',
                    help='target db name')       
    return parser.parse_args()

def main():
    tsfm = transformer.Transformer()
    (options, args) = init_option()
    tsfm.run(options)
    

if __name__ == '__main__':
    main()
