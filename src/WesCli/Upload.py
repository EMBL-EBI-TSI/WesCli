import requests


def upload(url, filename):
    
    with open(filename, 'rb') as f:
        
        r = requests.post( url, files = {'file': f} )
    
    
#     print(r)
     
    r.raise_for_status()
    
