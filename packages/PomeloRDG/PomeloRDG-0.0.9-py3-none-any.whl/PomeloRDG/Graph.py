import random
import PomeloRDG.Const as Const
import PomeloRDG.Utils as Utils

class Graph():
    def __init__(self, nsize, msize, **kwargs):
        self.nsize = nsize
        self.msize = msize if msize > 0 and msize <= (self.nsize) * (self.nsize - 1) // 2 else Utils.randint(self.nsize, (self.nsize) * (self.nsize - 1) // 2)
        self.directed = kwargs.get("directed", False)
        self.selflp = kwargs.get("selflp", False)
        self.rpedges = kwargs.get("rpedges", False)
        self.wtype = kwargs.get("wtype", int)
        self.weight = kwargs.get("weight", [Const.INT_MIN, Const.INT_MAX])
        self.value = self.__rand__() 
    
    def __rand__(self):
        """
        Generate a legal graph.
        """
        
        n, m, cnt = self.nsize, self.msize, 0
        self.value, used = {i: [] for i in range(1, n + 1)}, set()
        edges = [(i, j) for i in range(1, n + 1) for j in range(1, n + 1) if not self.selflp and i != j]
        random.shuffle(edges)
        
        for edge in edges:
            u, v = edge[0], edge[1]
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            if (not self.directed and ((u, v) in used or (v, u) in used)) and (not self.rpedges and (u, v) in used):
                continue
            if self.directed:
                used.add((u, v))
            else:
                used.add((u, v)); used.add((v, u))
            self.value[u].append((v, w))
            cnt += 1
            if cnt >= m:
                break
        return self.value
            
    def __str__(self):
        """
        Return the value in string type.
        """
        
        return self.to_str()
                    
    def get(self):
        """
        Return the value.
        """
        
        edges = []
        for u in self.value:
            for v in self.value[u]:
                edges.append((u, v[0], v[1]))
        return (self.nsize, self.msize, edges)
    
    def to_str(self, shuffle = True):
        """
        Change the value to OI format.
        """
        
        value = self.get(); n, m, g, res = value[0], value[1], value[2], ""
        res += "{} {}\n".format(str(n), str(m))
        if shuffle:
            random.shuffle(g)
        for edge in g:
            res += str(edge[0]) + " " + str(edge[1]) + " " + (str((edge[2])) if edge[2] != None else "") + "\n"
        return res
    
class Tree():
    def __init__(self, nsize, chain, flower, **kwargs):
        self.nsize = nsize
        self.chain = chain
        self.flower = flower
        self.directed = kwargs.get("directed", False)
        self.wtype = kwargs.get("wtype", int)
        self.weight = kwargs.get("weight", [Const.INT_MIN, Const.INT_MAX])
        self.value = self.__rand__()
        
    def __rand__(self):
        """
        Generate a legal Tree.
        """
        
        n = self.nsize
        chain_cnt, flower_cnt = int((n - 1) * self.chain), int((n - 1) * self.flower)
        self.value = {i: [] for i in range(1, n + 1)}
        
        if chain_cnt > n - 1:
            chain_cnt = n - 1
        if chain_cnt + flower_cnt > n - 1:
            flower_cnt = n - 1 - chain_cnt
        rand_cnt = n - 1 - chain_cnt - flower_cnt
        
        for i in range(2, chain_cnt + 2):
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            self.value[i - 1].append((i, w))
        
        for i in range(chain_cnt + 2, chain_cnt + flower_cnt + 2):
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            self.value[1].append((i, w))
        
        for i in range(n - rand_cnt + 1, n + 1):
            u = random.randrange(1, i)
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            self.value[u].append((i, w))
        
        return self.value
    
    def __str__(self):
        """
        Return the value in string type.
        """
        
        return self.to_str()
                    
    def get(self):
        """
        Return the value.
        """
        
        edges = []
        for u in self.value:
            for v in self.value[u]:
                edges.append((u, v[0], v[1]))
        return (self.nsize, self.nsize - 1, edges)
    
    def to_str(self, shuffle = True):
        """
        Change the value to OI format.
        """
        
        value = self.get(); n, m, g, res = value[0], value[1], value[2], ""
        res += "{} {}\n".format(str(n), str(m))
        if shuffle:
            random.shuffle(g)
        for edge in g:
            res += str(edge[0]) + " " + str(edge[1]) + " " + (str((edge[2])) if edge[2] != None else "") + "\n"
        return res

class Chain():
    def __init__(self, nsize, **kwargs):
        self.nsize = nsize
        self.directed = kwargs.get("directed", False)
        self.wtype = kwargs.get("wtype", int)
        self.weight = kwargs.get("weight", [Const.INT_MIN, Const.INT_MAX])
        self.value = Tree(self.nsize, 1, 0, directed = self.directed, wtype = self.wtype, weight = self.weight).value
        
    def __str__(self):
        """
        Return the value in string type.
        """
        
        return self.to_str()
                    
    def get(self):
        """
        Return the value.
        """
        
        edges = []
        for u in self.value:
            for v in self.value[u]:
                edges.append((u, v[0], v[1]))
        return (self.nsize, self.nsize, edges)
    
    def to_str(self, shuffle = True):
        """
        Change the value to OI format.
        """
        
        value = self.get(); n, m, g, res = value[0], value[1], value[2], ""
        res += "{} {}\n".format(str(n), str(m))
        if shuffle:
            random.shuffle(g)
        for edge in g:
            res += str(edge[0]) + " " + str(edge[1]) + " " + (str((edge[2])) if edge[2] != None else "") + "\n"
        return res
    
class Flower():
    def __init__(self, nsize, **kwargs):
        self.nsize = nsize
        self.directed = kwargs.get("directed", False)
        self.wtype = kwargs.get("wtype", int)
        self.weight = kwargs.get("weight", [Const.INT_MIN, Const.INT_MAX])
        self.value = Tree(self.nsize, 0, 1, directed = self.directed, wtype = self.wtype, weight = self.weight).value
        
    def __str__(self):
        """
        Return the value in string type.
        """
        
        return self.to_str()
                    
    def get(self):
        """
        Return the value.
        """
        
        edges = []
        for u in self.value:
            for v in self.value[u]:
                edges.append((u, v[0], v[1]))
        return (self.nsize, self.nsize - 1, edges)
    
    def to_str(self, shuffle = True):
        """
        Change the value to OI format.
        """
        
        value = self.get(); n, m, g, res = value[0], value[1], value[2], ""
        res += "{} {}\n".format(str(n), str(m))
        if shuffle:
            random.shuffle(g)
        for edge in g:
            res += str(edge[0]) + " " + str(edge[1]) + " " + (str((edge[2])) if edge[2] != None else "") + "\n"
        return res
    
class HSGraph():
    def __init__(self, nsize, **kwargs):
        self.nsize = nsize
        self.directed = kwargs.get("directed", False)
        self.selflp = kwargs.get("selflp", False)
        self.rpedges = kwargs.get("rpedges", False)
        self.wtype = kwargs.get("wtype", int)
        self.weight = kwargs.get("weight", [Const.INT_MIN, Const.INT_MAX])
        self.extraedges = kwargs.get("extraedges", 3)
        self.value = self.__rand__()
        
    def __rand__(self):
        """
        Generate a legal hack_spfa_graph.
        """
        
        n = self.nsize
        point_to_skip = n + 3 if not n % 2 else n / 2 + 1
        self.value, used = {i: [] for i in range(1, n + 1)}, set()
        
        for i in range(1, n // 2):
            (u, v) = (i + (i >= point_to_skip), i + 1 + (i + 1 >= point_to_skip))
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            if ((not self.directed and ((u, v) in used or (v, u) in used)) and (not self.rpedges and (u, v) in used)) or (not self.selflp and u == v):
                i -= 1
                continue
            if self.directed:
                used.add((u, v))
            else:
                used.add((u, v)); used.add((v, u))
            self.value[u].append((v, w))
            
            (u, v) = (i + n // 2 + ((i + n // 2) >= point_to_skip), i + n // 2 + 1 + ((i + n // 2 + 1) >= point_to_skip))
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            if ((not self.directed and ((u, v) in used or (v, u) in used)) and (not self.rpedges and (u, v) in used)) or (not self.selflp and u == v):
                i -= 1
                continue
            if self.directed:
                used.add((u, v))
            else:
                used.add((u, v)); used.add((v, u))
            self.value[u].append((v, w))
            
        for i in range(1, n // 2 + 1):
            (u, v) = (i + (i >= point_to_skip), i + n // 2 + ((i + n // 2) >= point_to_skip))
            w = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            if ((not self.directed and ((u, v) in used or (v, u) in used)) and (not self.rpedges and (u, v) in used)) or (not self.selflp and u == v):
                i -= 1
                continue
            if self.directed:
                used.add((u, v))
            else:
                used.add((u, v)); used.add((v, u))
            self.value[u].append((v, w))
            
        for i in range(self.extraedges):
            u = random.randint(1, n)
            v = random.randint(1, n)
            w  = self.wtype(Utils.randfloat(self.weight[0], self.weight[1])) if self.weight else None
            if ((not self.directed and ((u, v) in used or (v, u) in used)) and (not self.rpedges and (u, v) in used)) or (not self.selflp and u == v):
                i -= 1
                continue
            if self.directed:
                used.add((u, v))
            else:
                used.add((u, v)); used.add((v, u))
            self.value[u].append((v, w))
            
        return self.value
    
    def __str__(self):
        """
        Return the value in string type.
        """
        
        return self.to_str()
                    
    def get(self):
        """
        Return the value.
        """
        
        edges, cnt = [], 0
        for u in self.value:
            for v in self.value[u]:
                edges.append((u, v[0], v[1])); cnt += 1
        return (self.nsize, cnt, edges)
    
    def to_str(self, shuffle = True):
        """
        Change the value to OI format.
        """
        
        value = self.get(); n, m, g, res = value[0], value[1], value[2], ""
        res += "{} {}\n".format(str(n), str(m))
        if shuffle:
            random.shuffle(g)
        for _ in g:
            res += str(_[0]) + " " + str(_[1]) + " " + (str((_[2])) if _[2] != None else "") + "\n"
        return res