from langchain.embeddings.base import Embeddings
from langchain.text_splitter import CharacterTextSplitter
from typing import Any, List, Mapping, Optional,Tuple
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.document_loaders import DirectoryLoader
import requests
import json
from langchain.vectorstores import FAISS

from byzerllm.chatglm6b.tunning.infer import init_model as init_chatbot_model
from dataclasses import dataclass

@dataclass
class ClientParams:
    owner:str="admin"    


class ByzerLLMClient:
    
    def __init__(self,url:str='http://127.0.0.1:9003/model/predict',params:ClientParams=ClientParams()) -> None:
        self.url = url
        self.client_params = params

    def request(self, sql:str,json_data:str)->str:         
        data = {
            'sessionPerUser': 'true',
            'sessionPerRequest': 'true',
            'owner': self.client_params.owner,
            'dataType': 'string',
            'sql': sql,
            'data': json_data
        }
        response = requests.post(self.url, data=data)
        return response.text

    def emb(self,s:str)-> List[float]:
        json_data = json.dumps([
            {"instruction":s,"embedding":True}
        ])
        response = self.request('''
        select chat(array(feature)) as value
        ''',json_data)    
        t = json.loads(response)
        t2 = json.loads(t[0]["value"][0])
        return t2[0]["predict"]

    def chat(self,s:str,history:List[Tuple[str,str]])->str:
        newhis = [{"query":item[0],"response":item[1]} for item in history]
        json_data = json.dumps([
            {"instruction":s,"history":newhis,"output":"NAN"}
        ])
        response = self.request('''
        select chat(array(feature)) as value
        ''',json_data)    
        t = json.loads(response)
        t2 = json.loads(t[0]["value"][0])
        return t2[0]["predict"]


class LocalEmbeddings(Embeddings):
    def __init__(self,client:ByzerLLMClient):
        self.client = client
                
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:        
        embeddings = [self.client.emb(text) for text in texts]
        return embeddings

    def embed_query(self, text: str) -> List[float]:    
        embedding = self.client.emb(text)
        return embedding


class Chatglm6bLLM(LLM):
    
    n: int
        
    @property
    def _llm_type(self) -> str:
        return "chatglm6b"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return chat(prompt,[])
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n}


class VectorDB:
    def __init__(self,db_dir:str,client:ByzerLLMClient) -> None:
        self.db_dir = db_dir 
        self.db = None  
        self.client = client     

    def save(self,doc_dir:str,glob:str):
        loader = DirectoryLoader(doc_dir, glob=glob)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=30)
        split_docs = text_splitter.split_documents(documents) 
        embeddings = LocalEmbeddings(self.client)        
        db = FAISS.from_documents(split_docs, embeddings)
        db.save_local(self.db_dir) 

    def query(self,prompt:str,s:str):
        if not self.db:
           self.db = FAISS.load_local(self.db_dir)        
        result = self.db.similarity_search_with_score(prompt + s)
        return result






