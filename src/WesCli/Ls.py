from mypy_extensions import TypedDict
import requests
from WesCli.exception import UserMessageException



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


def ls(wesUrl) -> [DirEntry]:
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
    
    if r.status_code != requests.codes.ok:      # @UndefinedVariable
        
        raise UserMessageException(r.text)
    

    return r.json()
    
    
def cmd(url):
    
    entries = ls(url)
    
    print('\n'.join([formatEntry(e) for e in entries]))

