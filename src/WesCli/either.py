

class Either(object):
    
    def isOk(self):
        
        return type(self) == Ok


class Ok(Either):
    def __init__(self, v): self.v = v
    
    def __str__(self, *args, **kwargs):
        
        return f"Ok({self.v})"


class Error(Either):
    def __init__(self, v): self.v = v

    def __str__(self, *args, **kwargs):
        
        return f"Error({self.v})"




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

