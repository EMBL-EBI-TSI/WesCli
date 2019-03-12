# encoding: utf-8

import sys
from WesCli.ArgParser import getOpts
from WesCli.WesCli import run_multiple, status, status_multiple


def main(args):
    
    opts = getOpts(args)
    
#     print(opts)
    
    if   opts['run']    :    run_multiple(opts['<runSpec>'])
    elif opts['status'] :    status_multiple()
    
    
        

    
        
        


def entryPoint():
    return main(sys.argv[1:])

if __name__ == '__main__':
    entryPoint()