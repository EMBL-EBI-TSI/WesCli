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
    wes download [-p|--progress] [-d <location>|--destination=<location>] <url>
    wes upload <filename> <url>

Options:
  -h --help                                                     Shows this screen.
  -p --progress                                                 Display progress bar when downloading file
  -d <location> --destination <location>                        Designate a destination when downloading file

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
