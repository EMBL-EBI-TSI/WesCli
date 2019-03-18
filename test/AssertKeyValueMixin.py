

class AssertKeyValueMixin(object):
    
    def assertKeyValue(self, args, key, value):
        
        return self.assertEquals(args[key], value)



