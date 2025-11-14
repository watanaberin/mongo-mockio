import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import mockio.extensions
from optparse import OptionParser
from mockio.core.transformer import Transformer
from mockio.core.op import Op
from mockio.core.client import MongoDBclient
import json
from dotenv import load_dotenv
load_dotenv()

def init_option():
    # Get defaults from environment variables, falling back to hardcoded defaults
    filepath_default = os.getenv('TEMPLATE_FILE', 'template.json')
    num_default = int(os.getenv('MOCK_NUMBER', '100'))
    uri_default = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    db_default = os.getenv('MONGODB_DATABASE', 'test')

    parser = OptionParser()
    parser.add_option('-f', '--filepath',
                      dest='filepath',
                      default=filepath_default,
                      help='template json file path')

    parser.add_option('-n', '--num',
                      dest='num',
                      type='int',
                      default=num_default,
                      help='how many datas need mock into per collection')

    parser.add_option('-u',
                      '--uri',
                      dest='uri',
                      type='str',
                      default=uri_default,
                      help='MongoDB Uri: mongodb://user:password@example.com/?authSource=the_database&authMechanism=SCRAM-SHA-256')

    parser.add_option('-d',
                      '--db',
                      dest='db',
                      type='str',
                      default=db_default,
                      help='database name: test')

    return parser.parse_args()

def main():
    (options, args) = init_option()
    try:
        with open(options.filepath, 'r', encoding='utf-8') as f:
            template = json.load(f)
    except FileNotFoundError:
        print(f"Error: Template file '{options.filepath}' not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in template file: {str(e)}")
        return
    except Exception as e:
        print(f"Error reading template file: {str(e)}")
        return

    op: Op = Op(template, options.uri, options.db, options.num)
    if not op.client.is_connect() or not op.client.is_writable():
        print("Error: MongoDB is not connectable or writable")
        return
    Transformer(op).run()
        
if __name__ == '__main__':
    main()
