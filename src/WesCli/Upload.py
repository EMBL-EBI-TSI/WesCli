import requests
from os.path import basename
from urllib.parse import urljoin



def appendFilename(filename, url):

    return urljoin(url, basename(filename)) 


def isDir(url):

    return url[-1] == '/'


def upload(filename, url):

    if isDir(url):

        url = appendFilename(filename, url)


    _upload(filename, url)


def _upload(filename, url):

    with open(filename, 'rb') as f:

        r = requests.post( url, data = f )


#     print(r)

    r.raise_for_status()
