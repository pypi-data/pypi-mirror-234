from langchain.embeddings.openai import OpenAIEmbeddings
import tiktoken
from abc import ABC, abstractmethod
from os import getenv


tokenizer = tiktoken.get_encoding('cl100k_base')


class Vectorizer(ABC):
    def __init__(self, index_name=None, chunk_size=1000, chunk_overlap=0, separator=".", embeddings=None):
        self.index_name = index_name if index_name else getenv("INDEX_NAME")
        self.vectorstore = None
        self.vectorstore_index = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator

        if self.index_name is None:
            raise ValueError("index_name must be provided or INDEX_NAME environment variable must be set")

        if(embeddings is None):
            if getenv("OPENAI_EMBEDDINGS_DEPLOYMENT") :
                self.embeddings = OpenAIEmbeddings(deployment=getenv("OPENAI_EMBEDDINGS_DEPLOYMENT"))
            else :
                self.embeddings = OpenAIEmbeddings()
        else :
            self.embeddings = embeddings
        
    @abstractmethod
    def add_embeddings(self, ids, embeddings, metadatas, batch_size=50):
        pass

    @abstractmethod
    def search(self, query, top_k1=5, vector=None, filter=None, with_scores=False):
        pass
    
    # def search_and_rerank(self, query, top_k1 = 50, top_k2=5, filter=None):
    #     """
    #     Search and rerank the results with cohere
    #     """
    #     documents = self.search(query, top_k1, filter=filter)
    #     texts = list(map(lambda x: x["text"], documents))
    #     reranked_docs = compressor.client.rerank(model="rerank-multilingual-v2.0", query=query, documents=texts, top_n=top_k2)
    #     return list(map(lambda x: documents[x.index], reranked_docs))
        


