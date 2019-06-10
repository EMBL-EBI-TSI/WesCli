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
    wes download [-p] <url>
    wes upload <url> <filename>

Options:
  -h --help                          Shows this screen.
  -p                                 Display progress bar when downloading file
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
