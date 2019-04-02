from mypy_extensions import TypedDict
import requests
from WesCli.exception import UserMessageException
import os
from WesCli.url import getPath
from typing import List



class DirEntry(TypedDict):
    Name  : str
    IsDir : bool


def formatEntry(e: DirEntry):
    '''
    {
        "Mode" : 2151678445,
        "IsDir" : true,
        "ModTime" : "2019-03-14T14:30:56.919954122Z",
        "URL" : "./0PR0GE/",
        "Size" : 4096,
        "IsSymlink" : false,
        "Name" : "0PR0GE"
    }
    '''
    
    maybeSlash = '/' if e['IsDir'] else ''
    
    return e['Name'] + maybeSlash


def newFormatLine(wesUrl):
    
    basePath = getPath(wesUrl)
    
    def fileUrl(filename):
        
        return f"file:/{os.path.join(basePath, filename)}"


    def formatLine(e):
    
        filename = formatEntry(e)
        
        return f'{filename: <30} ({fileUrl(filename)})'
    
    
    return formatLine


def printDir(entries : [DirEntry], wesUrl):
    '''
    $ wes get https://tes.tsi.ebi.ac.uk/data/tmp/0PR0GE/
    
    tmp2ri6hb_r/        (file://data/tmp/0PR0GE/tmp2ri6hb_r/)
    tmp6awdshnf/        (file://data/tmp/0PR0GE/tmp.../)
    tmp_a_c9ltp/        (file://data/tmp/0PR0GE/tmp.../)
    tmppeev59oa/        (file://data/tmp/0PR0GE/tmp.../)
    '''
    
    formatLine = newFormatLine(wesUrl)
    
    print('\n'.join([formatLine(e) for e in entries]))


def _get(wesUrl):
    '''
    $ curl -H 'Accept: application/json' https://tes.tsi.ebi.ac.uk/data/tmp/ | json_pp 
    
    [
       {
          "Mode" : 2151678445,
          "IsDir" : true,
          "ModTime" : "2019-03-14T14:30:56.919954122Z",
          "URL" : "./0PR0GE/",
          "Size" : 4096,
          "IsSymlink" : false,
          "Name" : "0PR0GE"
       },
       {
          "Name" : "0UHH8N",
          "IsSymlink" : false,
          "IsDir" : true,
          "Mode" : 2151678445,
          "ModTime" : "2019-03-14T16:40:39.206135585Z",
          "Size" : 4096,
          "URL" : "./0UHH8N/"
       },
       {
          "Size" : 4096,
          "URL" : "./1NV7CL/",
          "Mode" : 2151678445,
          "IsDir" : true,
          "ModTime" : "2019-03-14T07:57:50.739277719Z",
          "IsSymlink" : false,
          "Name" : "1NV7CL"
       },
       .
       .
       .
    ]

    '''
    r = requests.get(wesUrl, headers = {'Accept': 'application/json'})
    
#     print(r)
    
    r.raise_for_status()
    
    return r


def getCmd(wesUrl):
    
    r = _get(wesUrl)

    contentType = r.headers['Content-Type']
    
    if contentType.startswith('application/json')   : printDir(r.json(), wesUrl) 
    else                                            : print(r.text)

    
def cat(fileUrl) -> str:
    
    return _get(fileUrl).text


def ls(dirUrl) -> List[DirEntry]:
    
    return _get(dirUrl).json()

