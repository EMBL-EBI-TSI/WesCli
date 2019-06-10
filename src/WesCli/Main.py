# encoding: utf-8

import sys
from WesCli.ArgParser import getOpts, hasWatch
from WesCli.WesCli import run_multiple, status_multiple
from WesCli.Get import getCmd, download
from WesCli.Upload import upload
import os


def main(args):
    
    try:
        _main(args)
    
    except Exception as e:
        
        print(e)
        
    
def _main(args):
    
    opts = getOpts(args)
    
#     print(opts)
    
    if   opts['run']    :    run_multiple(opts['<runSpec>'])
    elif opts['get']    :    getCmd(opts['<url>'])
    elif opts['upload'] :    upload(opts['<url>'], opts['<filename>'])
    elif opts['download'] :  download(opts['<url>'], opts['-p'])
    elif opts['status'] :    
        
        if hasWatch(opts) : os.system('watch -n 1 -d wes status')
        else              : status_multiple()


def entryPoint():
    return main(sys.argv[1:])

if __name__ == '__main__':
    entryPoint()
