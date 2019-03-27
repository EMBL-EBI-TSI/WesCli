from urllib.parse import urlsplit



def getPath(url):
    
    return urlsplit(url).path


def getBaseUrl(url):
    
#     print(urlsplit(url))  # SplitResult(scheme='https', netloc='tes.tsi.ebi.ac.uk', path='/ga4gh/wes/v1', query='', fragment='')
    
    parts = urlsplit(url)
    
    return f'{parts.scheme}://{parts.netloc}/'

