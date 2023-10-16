from langchain.embeddings.openai import OpenAIEmbeddings
import tiktoken
from wonkaai.Vectorizer.vectorizer import Vectorizer
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.models import Vector  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.models import Vector  
from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SearchField,  
    SemanticSettings,  
    SearchSuggester,
    VectorSearch,  
    HnswVectorSearchAlgorithmConfiguration,  
) 
from tqdm import tqdm
from os import getenv


tokenizer = tiktoken.get_encoding('cl100k_base')


class VectorizerCS(Vectorizer) : 
    """
    Vectorizer class
    """

    def __init__(self, index_name=None, chunk_size=1000, 
                 chunk_overlap=0, separator=".", azure_key=None, 
                 azure_endpoint=None, embeddings=None):
        """

        Args:
            index_name ([type]): index name in which data will be stored and retrieved
            azure_key (str, optional): Azure key to connect to pinecone. Defaults to "".
            azure_enpoint (str, optional): Azure endpoint. Defaults to "".
            embeddings ([type], optional): Required if you want to use a specific embedder. Defaults to None.
        """
        super().__init__(index_name, chunk_size, 
                         chunk_overlap, separator, embeddings)
        
        self.azure_key = azure_key if azure_key else getenv("SEARCH_API_KEY")
        self.azure_endpoint = azure_endpoint if azure_endpoint else getenv("SEARCH_ENDPOINT")

        if self.azure_key is None:
            raise ValueError("azure_key must be provided or SEARCH_API_KEY environment variable must be set")
        if self.azure_endpoint is None:
            raise ValueError("azure_endpoint must be provided or SEARCH_ENDPOINT environment variable must be set")

        self.credentials = AzureKeyCredential(self.azure_key)
        self.index_client = SearchIndexClient(
            endpoint=self.azure_endpoint, credential=self.credentials)
        self.search_client = SearchClient(endpoint=self.azure_endpoint,  
                                   index_name=self.index_name, 
                                   credential=self.credentials)  
        
        if not self.is_index_exist():
            self.create_index()

    def is_index_exist(self):
        result = self.index_client.list_index_names()
        return self.index_name in result

     
    def create_index(self):
        """
        Creates the index
        """

        search_suggester = SearchSuggester(name="sg", source_fields=["content"])

        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
            SearchableField(name="content", type=SearchFieldDataType.String, suggseters=[search_suggester]),
            SimpleField(name="metadatas", type=SearchFieldDataType.String),
            SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=1536, vector_search_configuration="my-vector-config"),
        ]

        vector_search = VectorSearch(
            algorithm_configurations=[
                HnswVectorSearchAlgorithmConfiguration(
                    name="my-vector-config",
                    kind="hnsw",
                    parameters={
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 500,
                        "metric": "cosine"
                    }
                )
            ]
        )

        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=PrioritizedFields(
                prioritized_content_fields=[SemanticField(field_name="content")]
            ),
            suggesters = [search_suggester]
        )
        semantic_settings = SemanticSettings(configurations=[semantic_config])

# Create the search index with the semantic settings
        index = SearchIndex(name=self.index_name, fields=fields,
                            vector_search=vector_search, semantic_settings=semantic_settings)
        result = self.index_client.create_or_update_index(index)
        print(f' {result.name} created')

    def delete_index(self):
        """
        Deletes the index
        """
        result = self.index_client.delete_index(self.index_name)
        print(f' index deleted')
    
    def get_document(self, id):
        """Gets the document with the given id

        Args:
            id (str): Id of the document
        
        Returns:
            dict: Document with the given id
        
        """
        try :
            result = self.search_client.get_document(key=id)
            metadatas = json.loads(result['metadatas'])
            result['metadatas'] = metadatas
            return result
        except Exception as e:
            if isinstance(e, ResourceNotFoundError) :
                return None
            else :
                raise e
            

    def delete_documents(self, ids):
        """
        Deletes the documents with the given ids
        
        Args:
            ids ([list]): List of ids that you want to delete
        
        Raises:
            Exception: "ids must be an array"
        """

        if not isinstance(ids, list):
             raise Exception("ids must be an array")
        keys = []
        for id in ids:
            keys.append({"id" : id})
        self.search_client.delete_documents(keys)
        return
    

    def update_metadatas(self, ids, new_metadatas, replace=False):
        """Updates the metadatas of the documents with the given ids

        Args:
            ids ([list]]): List of ids that you want to update
            new_metadatas (list): List of metadatas that you want to insert or replace
            replace (bool, optional): If true the old metadatas will be erased and replaced by the new_metadatas.
                                      If false the old metadatas and the new one will be merged.
                                      Defaults to False.

        Raises:
            Exception: "id and new_metadatas must be arrays"
            Exception: "id and new_metadatas must have the same length"
        """
        if(not isinstance(ids, list) or not isinstance(new_metadatas, list)):
             raise Exception("id and new_metadatas must be arrays")
        if(len(ids) != len(new_metadatas)):
             raise Exception("id and new_metadatas must have the same length")
        documents = []
        for i, id in enumerate(ids):
            if not replace :
                document = self.get_document(id)
                document["metadatas"] = json.dumps({**document["metadatas"], **new_metadatas[i]})
                documents.append(document)
            else :
                documents.append({"id" : id, "metadatas" : json.dumps(new_metadatas[i])})
        self.search_client.merge_documents(documents)


    def add_embeddings(self, ids, content, embeddings, metadatas, batch_size=50):
        """AI is creating summary for add_embeddings

        Args:
            ids (List): Id to upsert
            embeddings (List): Vectors embeddings to upsert
            metadatas (List): metadatas to upsert
            batch_size (int, optional): Defaults to 50.

        Returns:
            upserted_count: Number of upserted vectors
        """
        if(not isinstance(ids, list) or not isinstance(embeddings, list) or not isinstance(metadatas, list)):
             raise Exception("ids, embeddings and metadatas must be arrays")
        if(len(ids) != len(embeddings) or len(ids) != len(metadatas) or len(embeddings) != len(metadatas)):
             raise Exception("ids, embeddings and metadatas must have the same length")
        
        documents = []
        for i, v in enumerate(embeddings):
             document = {
                    "id" : str(ids[i]),
                    "content" : content[i],
                    "contentVector" : v, 
                    "metadatas" : json.dumps(metadatas[i])
             }
             documents.append(document)
        results = []
        for i in tqdm(range(0, len(documents), batch_size)):
            result = self.search_client.upload_documents(documents[i:i+batch_size])
            results += result
        
        return results

    def search(self, query, top_k1=5, vector=None, filter=None, with_scores=False):
        """AI is creating summary for search

        Args:
            query (sting): [description]
            top_k1 (int, optional): number of result to be returned. Defaults to 5.
            vector (list, optional): vector if already computed. Defaults to None.
            filter (list, optional): Pinecone filter to apply. Defaults to None.
            with_scores (bool, optional): If the results have to returned with the scores. Defaults to False.

        Returns:
           List: List of documents with their metadata, id and scores if with_scores is True
        """
        if(vector is None) :
            vector = Vector(value=self.embeddings.embed_query(query), k = top_k1, fields="contentVector")
            
        results = self.search_client.search(  
            search_text=None,  
            vectors= [vector],
            select=["id", "content", "metadatas", "contentVector"],
        )  
        vectors = []
        for result in results: 
            vectors.append({"id" : result['id'], "content" : result['content'], "metadatas" : json.loads(result['metadatas']), "score" : result['@search.score']})
        return vectors
        
if __name__ == "__main__":
    import os 
    index_name = "test-index2222222"
    v1 = Vectorizer_cs("27kquestion", index_name, azure_endpoint=os.environ["SEARCH_ENDPOINT"], azure_key=os.environ["SEARCH_API_KEY"])

