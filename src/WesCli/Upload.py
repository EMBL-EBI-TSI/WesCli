import requests


def upload(url, filename):
    
    with open(filename, 'rb') as f:
        
        r = requests.post( url, data = f )
    
    
#     print(r)
     
    r.raise_for_status()
    
