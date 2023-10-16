import pandas as pd
from wonkai.ResultAnalyser import ResultAnalyser
from wonkai.Dict import flatten_dict, deflatten_dict
import random
import string


class ResultComparator():
    
    def __init__(self) :
        column = ["key", "value", "perfect", "score", "is_in", "metadatas", "id"]
        self.df = pd.DataFrame(columns=column)

    def append_from_memory(self, memory, perfect_dict, metadatas={}, threshold=0.8) :
        result_analyser = ResultAnalyser()
        for m in memory :
            result_analyser.append_item(m)
        self.compare(result_analyser, perfect_dict, metadatas, threshold)

    def append_item(self, dict, perfect_dict, metadatas={}, threshold=0.8) :
        result_analyser = ResultAnalyser()
        result_analyser.append_item(dict)
        self.compare(result_analyser, perfect_dict, metadatas, threshold)
        
    def compare(self, result_analyser, perfect_dict, metadatas={}, threshold=0.8) :
        perfect_flat_dict = flatten_dict(perfect_dict)
        id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        for key, perfect_value in perfect_flat_dict.items() :
            value = result_analyser.get_value_max(key, threshold=threshold)
            is_in = perfect_value in list(result_analyser.get_values(key).keys()) 
            self.add(key, value, perfect_value, 1, is_in, metadatas, id)


    def add(self, key, value, perfect_value, score, is_in, metadatas, id) :
        self.df = pd.concat([self.df, pd.DataFrame([[key, value, perfect_value, score, is_in, metadatas, id]],
                                                    columns=self.df.columns)], ignore_index=True)
        
    def reset(self) :
        self.df = pd.DataFrame(columns=self.df.columns)
    
    def get_df(self):
        return self.df
    
    def compare_item(self, item1, item2) :
        if isinstance(item1, str) and isinstance(item2, str):
            return item1.lower() == item2.lower()
        else :
            return item1 == item2
        
    
    def get_rapport(self) :
        keys = self.df["key"].unique()
        rapport = pd.DataFrame(columns=["key", "good", "wrong", "under_threshold", "not_found", "is_in", "number", "accuracy", "raw_accuracy", "is_in_accuracy", "metadatas"])
        for key in keys :
            wrong_values = []
            df = self.df[self.df["key"] == key]
            good = 0
            number = len(df)
            wrong = 0
            under_threshold = 0
            not_found = 0  
            is_in = 0 
            for _, row in df.iterrows() :
                if self.compare_item(row["value"], row["perfect"]) :
                    good += 1
                elif row["value"] == "under_threshold" :
                    under_threshold += 1
                elif row['value'] == "not_found" : 
                    not_found += 1
                else :
                    wrong += 1
                    wrong_values.append({ "got" : row["value"], "expected" : row["perfect"], "metadatas" : row["metadatas"]})
                
                if row["is_in"] :
                    is_in += 1

            accuracy = good / max([(number-under_threshold-not_found),1])
            raw_accuracy = good / number
            is_in_accuracy = is_in / number
            rapport = pd.concat([rapport, pd.DataFrame([[key, good, wrong, under_threshold, not_found, is_in, number, accuracy, raw_accuracy, is_in_accuracy, wrong_values]],
                                                        columns=rapport.columns)], ignore_index=True)
        
        return rapport
            
            

