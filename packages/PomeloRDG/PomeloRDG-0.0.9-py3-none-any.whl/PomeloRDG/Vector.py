import PomeloRDG.Const as Const
import PomeloRDG.Utils as Utils

class Vector():
    def __init__(self, size, **kwarg):
        self.size = size
        self.type = kwarg.get("type", int)
        self.limit = kwarg.get("limit", [Const.INT_MIN, Const.INT_MAX])
        self.value = self.__rand__()
        
    def __rand__(self):
        """
        Generate a legal vector.
        """
        
        self.value = [self.type(Utils.randfloat(self.limit[0], self.limit[1])) for i in range(self.size)]
        return self.value
    
    def __check__(self, x):
        """
        Check if the vector elements are legal.
        """
        
        if Utils.list_like(x) or len(x) != self.size:
            return False
        for val in x:
            if type(val) != self.type:
                return False
        return True
    
    def __str__(self):
        """
        Return the value in string type.
        """
        
        return str(self.get())
        
    def get(self):
        """
        Return the value.
        """
        
        return [self.value[i] for i in range(self.size)]