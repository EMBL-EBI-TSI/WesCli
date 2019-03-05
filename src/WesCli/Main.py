# encoding: utf-8

import sys
from WesCli.ArgParser import getOpts
from WesCli.WesCli import run_multiple


def main(args):
    
    opts = getOpts(args)
    
#     print(opts)
    
#     {'<runSpec>': 'examples/sitesWithError.yaml',
#      'run': True}

    run_multiple(opts['<runSpec>'])
    
    
    
        

    
        
        


def entryPoint():
    return main(sys.argv[1:])

if __name__ == '__main__':
    entryPoint()
