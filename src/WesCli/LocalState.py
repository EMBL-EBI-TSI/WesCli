# encoding: utf-8

import json


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
        
    
    def add(self, url, idOrError): 
        
        self.sites.append({
            
            'url'         : url     
          , 'idOrError'   : idOrError
        })
        

    def save(self):
        
        with open(DOT_FILE, 'w') as f:
        
            json.dump(self.asDict(), f)
        
            
    def load(self):
            
        with open(DOT_FILE) as f:
        
            self.lists = json.load(f)
            

    def asDict(self):
        
        return {
            
            'workflowUrl'   : self.workflowUrl 
           ,'sites'         : self.sites
        }


    def __repr__(self):
        
        return str(self.asDict())

