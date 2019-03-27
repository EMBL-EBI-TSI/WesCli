# coding=utf-8

import sys
from docopt import docopt


def main():
    
    args = getOpts(sys.argv[1:])
    
    print(args)
    
    
def getOpts(args):
    
    doc = """
Usage:
    wes run <runSpec>
    wes status [-w|--watch]
    wes get <url>
    wes upload <url> <filename>


Options:
  -h --help                          Shows this screen.


"""
    
    
    return docopt(doc, argv=args)
    
    
def hasWatch(args):
    '''
    {'--watch': True,
     '-w': False,
     'status': True}
    '''

    return args.get('--watch') or \
           args.get('-w')
    
    


if __name__ == '__main__':
    main()
