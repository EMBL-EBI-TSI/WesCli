# encoding: utf-8

import yaml
from jinja2 import Template
import requests


def loadYaml(filename):
    
    with open(filename, 'r') as f:
        
        return yaml.safe_load(f)


def getEffectiveConf(conf):
    
    inputTemplate   = conf['inputTemplate']
    sites           = conf['sites']
    
    template = Template(inputTemplate)

    def renderSite(s):
        
        return {
            
            'url'   : s['url']
           ,'input' : template.render(s['inputTemplateParams'])
        }
        
    return {
        
        'workflow'  : conf['workflow']
       ,'sites'     : [ renderSite(s) for s in sites ]
    }


def run( wesUrl         : str
       , workflowUrl    : str
       , params         : str):
    
    '''
        curl -iv -X POST                                    \
             -H 'Content-Type: multipart/form-data'         \
             -H 'Accept: application/json'                  \
             -F workflow_params="$params"                   \
             -F workflow_type=cwl                           \
             -F workflow_type_version=v1.0                  \
             -F "workflow_url=$workflowUrl"                 \
             "$(wesUrl)/runs"
    '''
    
    r = requests.post(f"{wesUrl}/runs", data = {
        
          'workflow_type'           : 'cwl'         
         ,'workflow_type_version'   : 'v1.0'        
         ,'workflow_url'            : workflowUrl
         ,'workflow_params'         : params   
    })
    
    if   r.status_code == requests.codes.ok : return Ok(r.json())
    else                                    : return Error((r.status_code, r.text))    # TODO receive 2 args in __init__ ?


class Ok(object):
    def __init__(self, v): self.v = v
    
    def __str__(self, *args, **kwargs):
        
        return f"Ok({self.v})"


class Error(object):
    def __init__(self, v): self.v = v




# 
# 
# class Either(object):
#     pass
# 
# class Left(Either):
#     def __init__(self, v): self.v = v
#     def is_left(self): return True
#     def is_right(self): return False
#     def value(self): return self.v 
# 
# class Right(Either):
#     def __init__(self, v): self.v = v
#     def is_left(self): return False
#     def is_right(self): return True
#     def value(self): return self.v 

