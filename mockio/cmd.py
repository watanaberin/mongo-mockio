import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import mockio.extesions
from optparse import OptionParser
from mockio.core.transformer import Transformer
from mockio.core.op import Op
from mockio.core.client import MongoDBclient
import json
from dotenv import load_dotenv
load_dotenv()

def init_option():
    parser = OptionParser()
    parser.add_option('-f', '--filepath',
                      dest='filepath',
                      default='template.json',
                      help='template json file path')
    
    parser.add_option('-n', '--num',
                      dest='num',
                      type='int',
                      default=100,
                      help='how many datas need mock into per collection')
    
    parser.add_option('-u',
                      '--uri',
                      dest='uri',
                      type='str',
                      default="mongodb://localhost:27017",
                      help='MongDB Uri: mongodb://user:password@example.com/?authSource=the_database&authMechanism=SCRAM-SHA-256')
    
    parser.add_option('-d',
                      '--db',
                      dest='db',
                      type='str',
                      default='test',
                    help='database name: test')
    
    if not parser.has_option('filepath') and os.getenv('TEMPLATE_FILE'):
        parser.set_default('filepath', os.getenv('TEMPLATE_FILE'))
        
    if not parser.has_option('num') and  os.getenv('MOCK_NUMBER'):
        parser.set_default('num', os.getenv('MOCK_NUMBER'))

    if not parser.has_option('uri') and os.getenv('MONGODB_URI') :
        parser.set_default('uri', os.getenv('MONGODB_URI'))
        
    if not parser.has_option('db'):
        parser.set_default('db', os.getenv('MONGODB_DATABASE'))
    
    return parser.parse_args()

def main():
    (options, args) = init_option()
    with open(options.filepath, 'r') as f:
        template = json.load(f)
    op: Op = Op(template, options.uri, options.db, options.num)
    if not op.client.is_connect() or not op.client.is_writable():
        return
    Transformer(op).run()
        
if __name__ == '__main__':
    main()
