import requests
from os.path import basename
from urllib.parse import urljoin



def appendFilename(url, filename):
    
    return urljoin(url, basename(filename))


def isDir(url):
    
    return url[-1] == '/'


def upload(url, filename):
    
    if isDir(url): 
        
        url = appendFilename(url, filename)
    
    
    _upload(url, filename)
    
    
def _upload(url, filename):
    
    with open(filename, 'rb') as f:
        
        r = requests.post( url, data = f )
    
    
#     print(r)
     
    r.raise_for_status()
    
