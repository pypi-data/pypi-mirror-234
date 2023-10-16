from langchain.chat_models import ChatOpenAI
from os import getenv
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import openai
import time


class ChatFunction():

    def __init__(self, prompt_template, **kwargs) :

        if "model" not in kwargs and "deployment_id" not in kwargs :
            kwargs["model"] = "gpt-3.5-turbo-0613"

        self.kwargs = kwargs
        
        self.prompt_template = prompt_template

    def _format_prompt(self, input):
        s = self.prompt_template.format_messages(**input)
        ss = []
        for i in s : 
            if isinstance(i, SystemMessage):
                ss.append({"role" : "system", "content" : i.content})
            elif isinstance(i, HumanMessage):
                ss.append({"role" : "user", "content" : i.content})
            elif isinstance(i, AIMessage):
                ss.append({"role" : "assistant", "content" : i.content})
            
        return(ss)

    def generate(self, function_schema = [], no_error=True, retry=5, **kwargs):
        try :
            if retry < 0 :
                raise ValueError("Too many retries")
            if len(function_schema) == 0  :
                raise ValueError("No function schema")
            response = openai.ChatCompletion.create(
                **self.kwargs,
                messages=self._format_prompt(kwargs),
                functions=function_schema,
                function_call={"name" : function_schema[0]["name"]},
            ) 
            return response
        except openai.error.RateLimitError as e:
            print("Rate Limit Error, retrying in {} seconds".format(4*(5-retry+1)))
            time.sleep(4*(5-retry+1))
            self.generate(function_schema, no_error, retry=retry-1, **kwargs)
        except openai.error.ServiceUnavailableError as e :
            print("Rate Limit Error, retrying in {} seconds".format(4*(5-retry+1)))
            time.sleep(4*(5-retry+1))
            self.generate(function_schema, no_error, retry=retry-1, **kwargs)
            raise openai.error.RateLimitError("Unstable Error: " + str(e)) from e
        
        except Exception as e:
            if no_error:
                print(e)
                return("ERROR")
            else :
                raise e