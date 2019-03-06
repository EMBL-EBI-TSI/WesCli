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
    wes status <runId>


Options:
  -h --help                          Shows this screen.


"""
    
    
    return docopt(doc, argv=args)
    
    


if __name__ == '__main__':
    main()
