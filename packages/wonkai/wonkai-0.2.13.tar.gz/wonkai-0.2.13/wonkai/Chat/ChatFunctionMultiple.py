from wonkai.Chat import ChatFunction
from wonkai.ResultAnalyser import ResultAnalyser
import json

class ChatFunctionMultiple(ChatFunction):

    def __init__(self, prompt_template, n=10, result_analyser=None, **kwargs):
        super().__init__(prompt_template, n=n, **kwargs)
        self.result_analyser = result_analyser

    def generate(self, function_schema=..., no_error=True, threshold=0.8, result_analyser=None, **kwargs):
        response = super().generate(function_schema, no_error, **kwargs)

        if response == "ERROR":
            return None
        
        if response.get("choices") is None:
            return None
        
        choices = response.get("choices")
        if self.result_analyser is None and result_analyser is None:
            result_analyser = ResultAnalyser()
        if result_analyser is None and self.result_analyser is not None:
            result_analyser = self.result_analyser

        arguments = []
        for choice in choices :
            message = choice.get("message")
            if message is None :
                result_analyser.append_item({"error" : "no message"})
                continue
            function_call = message.get("function_call")
            if function_call is None :
                result_analyser.append_item({"error" : "no function call"})
                continue   
            name = function_call.get("name")
            arguments =  function_call.get("arguments")
            if name is None or arguments is None :
                result_analyser.append_item({"error" : "no function name"})
                continue
            if name != function_schema[0]["name"] :
                result_analyser.append_item({"error" : "invalid function name"})
                continue
            if arguments is None :
                result_analyser.append_item({"error" : "no function arguments"})
                continue

            try :
                result_analyser.append_item(json.loads(arguments))
            except :
                result_analyser.append_item({"error" : "invalid json"})
                continue

        return result_analyser
                    
    
        
