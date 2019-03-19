# encoding: utf-8

import sys
from WesCli.ArgParser import getOpts
from WesCli.WesCli import run_multiple, status_multiple
from WesCli.exception import UserMessageException
from WesCli.Get import get
from WesCli.Upload import upload


def main(args):
    
    try:
        _main(args)
    
    except Exception as e:
        
        print(e)
        
    
def _main(args):
    
    opts = getOpts(args)
    
#     print(opts)
    
    if   opts['run']    :    run_multiple(opts['<runSpec>'])
    elif opts['status'] :    status_multiple()
    elif opts['get']    :    get(opts['<url>'])
    elif opts['upload'] :    upload(opts['<url>'], opts['<filename>'])
    
    
        

    
        
        


def entryPoint():
    return main(sys.argv[1:])

if __name__ == '__main__':
    entryPoint()
