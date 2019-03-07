# encoding: utf-8

import json
from WesCli.either import Either


DOT_FILE = '.wes'
        

class LocalState(object):
    '''
    Workflow url
    List:
        Site (wes base url)
        inputTemplateParams    TODO?
        runId
    '''
    
    def __init__(self, workflowUrl):
         
        self.workflowUrl = workflowUrl
        self.sites = []
        
    
    def add(self, url
                , idOrError: Either): 
        
        s = {
            
            'url'  : url
           ,'ok'   : True
           ,'id'   : idOrError.v
        
        } if idOrError.isOk() else {
            
            'url'   : url     
           ,'ok'    : False
           ,'error' : idOrError.v
        } 
        
        self.sites.append(s)
        

    def save(self):
        
        with open(DOT_FILE, 'w') as f:
        
            json.dump(self.asDict(), f)
        
            
    def load(self):
            
        with open(DOT_FILE) as f:
        
            d = json.load(f)
            
            self.workflowUrl = d['workflowUrl']
            self.sites       = d['sites']
            

    def asDict(self):
        
        return {
            
            'workflowUrl'   : self.workflowUrl 
           ,'sites'         : self.sites
        }


    def __repr__(self):
        
        return str(self.asDict())

