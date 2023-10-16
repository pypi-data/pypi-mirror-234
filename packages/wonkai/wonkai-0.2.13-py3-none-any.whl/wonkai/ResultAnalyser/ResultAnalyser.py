from copy import deepcopy
from wonkai.Dict import flatten_dict, deflatten_dict
from .ResultMemory import ResultMemory

class ResultAnalyser() :

    def __init__ (self) :
        self.results = []
        self.memory = []

    def append_item(self, dict):
        self.memory.append(dict)
        flat_dict = flatten_dict(dict)
        for key, value in flat_dict.items() :
            self.add(key, value)

    def add(self, key, value):
        for res in self.results :
            if res.equal_key(key) :
                res.add_value(value)
                return
        self.results.append(ResultMemory(key, value))

    
    def get_value_max(self, key, threshold=0.8, sep="___") :
        if isinstance(key, list) :
            key = sep.join(key)
        for i in self.results :
            if i.equal_key(key) :
                return i.get_value_max(threshold=threshold)
        return "not_found"

    def get_values_max(self, keys, threshold=0.8, sep="___") :
        values = {}
        key = sep.join(keys) + sep
        for i in self.results :
            if key == i.key[:len(key)] :
                values[i.key[len(key):]] = i.get_value_max(threshold=threshold)
        
        return deflatten_dict(values)
    
    def get_value_max_with_confidence(self, key, sep="___"):
        if isinstance(key, list) :
            key = sep.join(key)

        for i in self.results :
            if i.equal_key(key) :
                return i.get_higgest()
        return({"value" : "not_found", "score" : 0})

    def get_values_max_with_confidence(self, keys, sep="___"):
        values = {}
        key = sep.join(keys) + sep
        for i in self.results :
            if key == i.key[:len(key)] :
                values[i.key[len(key):]] = self.get_value_max_with_confidence(i.key)
        return deflatten_dict(values)
    
    def get_values(self, key):
        for i in self.results :
            if i.equal_key(key) :
                return i.get_values()
        return {"error" : "not_found"}
    

    def get(self, key, sep="___"):
        if isinstance(key, list) :
            key = sep.join(key)
        for i in self.results :
            if i.equal_key(key) :
                return i
        return None
    
    def get_multiple(self, keys, sep="___"):
        values = {}
        key = sep.join(keys) + sep
        for i in self.results :
            if key == i.key[:len(key)] :
                values[i.key[len(key):]] = i
        return values
            
    def to_dict(self) :
        d = {}
        for i in self.results :
            d[i.key] = i.to_dict()
        return d
    
    def from_dict(self, d) :
        dict = deflatten_dict(d)
        for key, value in dict.items() :
            self.results.append(ResultMemory(key, value))

    def from_memory(self, memory) :
        for item in memory :
            self.append_item(item)

    def get_memory(self) :
        return deepcopy(self.memory)