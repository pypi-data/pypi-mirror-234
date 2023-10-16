import random
import PomeloRDG.Const as Const

class String():
    def __init__(self, size = 0, charset = Const.CHARS):
        self.size = size
        self.charset = charset
        self.value = self.__rand__()
        
    def __rand__(self):
        res = ""
        for i in range(self.size):
            res += random.choice(self.charset)
        return res
    
    def __str__(self):
        return self.get()
    
    def get(self):
        return self.value