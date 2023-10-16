class ResultMemory() :

    def __init__(self, key, value) :
        self.res = {}
        self.key = key
        self.values = {}
        self.pourcentage = {}
        self.n = 0
        self.add_value(value)
    
    def add_value(self, value, avoid=["", None, "unknown", "UNKNOWN"]) :
        if value in avoid :
            return
        if self.values.get(value) is None :
            self.values[value] = 1
        else :
            self.values[value] += 1
        self.n += 1
        self.compute_pourcentage()
    
    def get_values(self) :
        return self.values
    
    def get_n(self) :
        return self.n
    
    def compute_pourcentage(self) :
        pourcentage = {}
        for key, value in self.values.items() :
            pourcentage[key] = value / self.n
        self.pourcentage = pourcentage
    
    def get_higgest(self) :
        if len(self.pourcentage) == 0 :
            return {"value" : "not_found", "score" : 0}
        return {"value" : max(self.pourcentage, key=self.pourcentage.get), "score" : self.pourcentage[max(self.pourcentage, key=self.pourcentage.get)]}
    
    def get_value_max(self, threshold=0.8) :
        if self.get_higgest()["score"] < threshold :
            return "under_threshold"
        else :
            return self.get_higgest()["value"]

    def equal_key(self, key):
        return self.key == key

    def to_dict(self) :
        return {
            "values" : self.values,
            "n" : self.n,
            "higgest" : self.get_higgest(),
            "pourcentage" : self.pourcentage,
            "key" : self.key
        }
        