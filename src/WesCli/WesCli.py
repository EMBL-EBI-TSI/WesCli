# encoding: utf-8

import yaml
from jinja2 import Template


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
