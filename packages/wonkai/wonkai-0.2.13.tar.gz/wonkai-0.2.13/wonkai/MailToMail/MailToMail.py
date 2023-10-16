from wonkaai.Vectorizer import VectorizerCS
from wonkaai.Prompt import STANDALONE_QUESTION_PROMPT
from wonkaai.Chat import Chat
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class MailToMail(VectorizerCS):

    def __init__(self, prompt=STANDALONE_QUESTION_PROMPT, chat_kwargs = {}, **kwargs):
        """
        Kwargs :
            index_name (str, optional): index name in which data will be stored and retrieved
            azure_key (str, optional): Azure key to connect to pinecone. Defaults to "".
            azure_enpoint (str, optional): Azure endpoint. Defaults to "".
            embeddings (str, optional): Required if you want to use a specific embedder. Defaults to None.
        """
        super().__init__(**kwargs)
        self.prompt = prompt
        self.chat_kwargs = chat_kwargs
        self.chat = Chat(self.prompt, **self.chat_kwargs)

    def get_standalone_question(self, mail):
        """
        Generate a standalone question from a mail
        Args:
            mail (str): mail from which the standalone question will be generated
        Returns:
            str: standalone question"""
        

        return self.chat.generate(input={"input" : mail})
    

    def get_standalone_questions(self, mails):
        """
        Generate a standalone question from a list of mails
        Args:
            mails (list): list of mails from which the standalone questions will be generated
        Returns:
            list: list of standalone questions
        """

        standalone_questions = []
        with ThreadPoolExecutor(max_workers=15) as executor:
            standalone_questions = list(tqdm(executor.map(self.get_standalone_question, mails)))
        return standalone_questions
    
    
    def get_embedding(self, contents):
        """
        Get embeddings from a list of contents
        Args:
            contents (list[str]): list of contents from which the embeddings will be generated
        Returns:
            dict: dict containing the embeddings and the error
        """

        total_ems = []
        error = []
        for i in tqdm(range(0, len(contents), 16)):
            try :
                total_ems += self.embeddings.embed_documents(contents[i:i+16])
            except Exception as e:
                error += range(i, i+16)
                print(e)
        return {"total_ems" : total_ems, "error" : error}

    def add_mails(self, ids, mails, metadatas):
        """
        Add mails to the index
        Args:
            ids (list[str]): list of ids
            mails (list[str]): list of mails
            metadatas (list[dict]): list of metadatas
        Returns:
            dict: dict containing the number of mails added and the index of the mail where an error occured
        """

        if len(ids) != len(mails) or len(ids) != len(metadatas) :
            raise Exception("ids, mails and metadatas must have the same length")
        standalone_questions = self.get_standalone_questions(mails)
        embeddings = self.get_embedding(standalone_questions)
        #remove from metadatas ids and content the error
        for i in sorted(embeddings['error'], reverse=True):
            del ids[i]
            del mails[i]
            del metadatas[i]
            del standalone_questions[i]

        res = self.add_embeddings(ids, standalone_questions, embeddings['total_ems'], metadatas)
        return({"number of mails added" : res, "error" : embeddings['error']})

    def add_mail(self, id, mail, metadatas):
        """
        Add a mail to the index
        Args:
            id (str): id
            mail (str): mail
            metadatas (dict): metadatas
            
        Returns:
            dict: dict containing mail added in format : IndexingResult class https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.models.indexingresult?view=azure-python
        """

        return self.add_mails([id], [mail], [metadatas])
    
    def search_mails(self, mails, top_k1=5, vector=None, filter=None, with_scores=True, thread=15, with_stand_alone_question=True):
        """
        Search mails in the index
        Args:
            mails (list[str]): list of mails
            top_k1 (int, optional): number of results to return. Defaults to 5.
            vector (str, optional): vector if already computed. Defaults to None.
            filter (str, optional): filter to use. Defaults to None.
            with_scores (bool, optional): whether to return scores. Defaults to True.
            thread (int, optional): number of threads to use. Defaults to 15.
        Returns:
            list[dict]: list of results
        """

        def search_mail_1(mail):
            res = self.search_mail(mail, top_k1, vector, filter, with_scores)
            return res
        
        results = []
        with ThreadPoolExecutor(max_workers=thread) as executor:
            results = list(tqdm(executor.map(search_mail_1, mails)))
        return results

    def search_mail(self, mail, top_k1=5, vector=None, filter=None, with_scores=True, with_stand_alone_question=True):
        """
        Search a mail in the index
        Args:
            mail (str): mail
            top_k1 (int, optional): number of results to return. Defaults to 5.
            vector (str, optional): vector if already computed. Defaults to None.
            filter (str, optional): filter to use. Defaults to None.
            with_scores (bool, optional): whether to return scores. Defaults to True.
        Returns:
            list[dict]: list of results
        """
        standalone_question = mail
        if with_stand_alone_question:
            standalone_question = self.get_standalone_question(mail)
        standalone_question = standalone_question.split("\n")[0].strip()
        return super().search(standalone_question, top_k1, vector, filter, with_scores)



        

