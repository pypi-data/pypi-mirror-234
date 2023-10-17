import datetime
from datetime import datetime as DateTime
from copy import deepcopy
import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from pydantic import Field

from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.schema import BaseRetriever, Document
from langchain.vectorstores.base import VectorStore
from langchain.retrievers import TimeWeightedVectorStoreRetriever

from companion_agent.myfaiss import MyFAISS


def _get_hours_passed(time: datetime.datetime, ref_time: datetime.datetime) -> float:
    """Get the hours passed between two datetime objects."""
    return (time - ref_time).total_seconds() / 3600


class ImportanceWeightedVectorStoreRetriever(TimeWeightedVectorStoreRetriever):
    """Retriever that combines embedding similarity with
    recency in retrieving values."""

    vectorstore: VectorStore = None
    """The vectorstore to store documents and determine salience."""

    search_kwargs: dict = {'k':100, 'fetch_k':100}
    """Keyword arguments to pass to the vectorstore similarity search."""

    # TODO: abstract as a queue
    memory_stream: dict = None
    """The memory_stream of documents to search through."""

    consciousness: List[int] = []
    """The memory_stream of documents to search through."""

    observations: List[int] = []
    """The memory_stream of documents to search through."""

    retrieve_count: int = 0

    decay_rate: float = 0.01
    """The exponential decay factor used as (1.0-decay_rate)**(hrs_passed)."""

    delay_rate: float = 0.3
    """The delay factor to control when the subject importance would be activated. The rate is aligned to the recency"""

    k: int = 4
    """The maximum number of documents to retrieve in a given call."""

    other_score_keys: List[str] = ['sub_imp', 'obj_imp']
    """Other keys in the metadata to factor into the score, e.g. 'sub_imp', 'obj_imp'."""

    default_salience: Optional[float] = None
    """The salience to assign memories not retrieved from the vector store.

    None assigns no salience to documents not fetched from the vector store.
    """
    importance_weight: Optional[float] = 0.5

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_memeory_stream(self):
        self.memory_stream = self.vectorstore.docstore.__dict__['_dict']
        return self.memory_stream

    def _update_subject_impotance(self, current_time = None):
        """update all documents' subject importance"""
        memory_stream = self.get_memeory_stream()
        docs = [doc for doc in memory_stream.values()]
        if not current_time: current_time = datetime.datetime.now()
        lifetime_list, hits_list = [], []
        for doc in docs:
            lifetime_list.append(self.retrieve_count - doc.metadata['started_at'])
            hits_list.append(doc.metadata["hits"])

        def _sigmoid(hours):
            offset = hours - math.log(self.delay_rate, (1-self.decay_rate))
            return 1/(1 + np.exp(-offset))
        
        def _softmax(x):
            y = np.exp(x - np.max(x))
            f_x = y / np.sum(y)
            return f_x
        
        def _l2_norm(x):
            l2 = np.linalg.norm(x)
            return x / (0.01 if not l2 else l2)
        
        lifetime_list, hits_list = np.array(lifetime_list), np.array(hits_list)
        sub_imp = np.power((1-self.decay_rate), lifetime_list - hits_list)
        # sub_imp = _l2_norm(sub_imp)
        for step, doc in enumerate(docs):
            doc.metadata["sub_imp"] = sub_imp[step]
        

    def _get_combined_score(
        self,
        document: Document,
        vector_relevance: Optional[float],
        current_time: datetime.datetime,
        importance_weight = None,
    ) -> float:
        """Return the combined score for a document."""
        if importance_weight == None: importance_weight = self.importance_weight
        hours_passed = _get_hours_passed(
            current_time,
            document.metadata["last_accessed_at"],
        )
        hours_passed_max = math.log(0.001, (1-self.decay_rate))
        # print(hours_passed)
        if hours_passed>=hours_passed_max: score = 0
        elif hours_passed<=0.001: score = 1
        else: score = (1.0 - self.decay_rate) ** hours_passed
        for key in self.other_score_keys:
            if key in document.metadata:
                score += document.metadata[key]
        importance = score / (len(self.other_score_keys)+1)
        score = importance * importance_weight
        if vector_relevance is not None:
            score += vector_relevance
        return score, importance


    def get_salient_docs(self, query: str) -> Dict[int, Tuple[Document, float]]:
        """Return documents that are salient to the query."""
        memory_stream = self.get_memeory_stream()
        docs_and_scores: List[Tuple[Document, float]]
        docs_and_scores = self.vectorstore.similarity_search_with_relevance_scores(
            query, **self.search_kwargs
        )
        results = {}
        for fetched_doc, relevance in docs_and_scores:
            if "buffer_idx" in fetched_doc.metadata:
                buffer_idx = fetched_doc.metadata["buffer_idx"]
                doc = memory_stream[buffer_idx]
                results[buffer_idx] = (doc, relevance)
        return results
    

    def _get_document_by_key(self, key: str, increase = False):
        memory_stream = self.get_memeory_stream()
        if key in memory_stream:
            doc = memory_stream[key]
            if increase: doc.metadata['hits'] += 1
            return doc
        
    
    def _get_documents_by_keys(self, keys: List[str] = []):
        memory_stream = self.get_memeory_stream()
        docs = []
        for key in keys:
            doc = memory_stream[key]
            docs.append(doc)
        return docs
    

    def _get_consciousness_importance(self, current_time: datetime.datetime = None):
        memory_stream = self.get_memeory_stream()
        if current_time is None:
            current_time = datetime.datetime.now()
        self._update_subject_impotance(current_time)
        return {key:self._get_combined_score(memory_stream[key],None,current_time, 1.0) for key in self.consciousness}
        

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun, top_k: int = None, importance_weight = None, threshold = None, time_sorted=None
    ) -> List[Document]:
        """Return documents that are relevant to the query."""
        if importance_weight == None: importance_weight = self.importance_weight
        if time_sorted == None: time_sorted = True
        memory_stream = self.get_memeory_stream()
        current_time = datetime.datetime.now()
        k = -top_k if top_k!=None else -self.k

        docs_and_scores = {
            key: (memory_stream[key], self.default_salience)
            for key in self.consciousness[k :]
        }
        
        # If a doc is considered salient, update the salience score
        docs_and_scores.update(self.get_salient_docs(query))
        # 更新主观重要性
        self._update_subject_impotance()
        rescored_docs = [
            (doc, *self._get_combined_score(doc, relevance*(1-importance_weight), current_time, importance_weight),relevance)
            for doc, relevance in docs_and_scores.values()
        ]
        rescored_docs.sort(key=lambda x: x[1], reverse=True)
        result = []
        self.retrieve_count += 1
        # Ensure frequently accessed memories aren't forgotten
        for doc, scores, _, _ in rescored_docs[: self.k]:
            if threshold and threshold > scores: return result
            # TODO: Update vector store doc once `update` method is exposed.
            buffered_doc = memory_stream[doc.metadata["buffer_idx"]]
            buffered_doc.metadata["last_accessed_at"] = current_time
            if not buffered_doc.metadata["hits"]: buffered_doc.metadata["hits"] = 1
            else: buffered_doc.metadata["hits"] += 1
            result.append(buffered_doc)
        if time_sorted: rescored_docs.sort(key=lambda x: x[0].metadata['created_at'])
        return result
    
    def add_observations(self, documents: List[Document], **kwargs: Any) -> List[str]:
        return self.add_documents(documents, isThought = False, **kwargs)
    
    def add_thoughts(self, documents: List[Document], **kwargs: Any) -> List[str]:
        return self.add_documents(documents, isThought = True, **kwargs)

    def add_documents(self, documents: List[Document], isThought = True, **kwargs: Any) -> List[str]:
        """Add documents to vectorstore."""
        current_time = kwargs.get("current_time")
        if current_time is None:
            current_time = datetime.datetime.now()
        # Avoid mutating input documents
        dup_docs = [deepcopy(d) for d in documents]
        for i, doc in enumerate(dup_docs):
            if "last_accessed_at" not in doc.metadata:
                doc.metadata["last_accessed_at"] = current_time
            if "created_at" not in doc.metadata:
                doc.metadata["created_at"] = current_time
            if "started_at" not in doc.metadata:
                doc.metadata["started_at"] = self.retrieve_count
            if "hits" not in doc.metadata:
                doc.metadata["hits"] = 0

        keys = self.vectorstore.add_documents(dup_docs, **kwargs)
        # dict_docs = {}
        for i, doc in enumerate(dup_docs):
            doc.metadata["buffer_idx"] = keys[i]
            if isThought: self.consciousness.append(doc.metadata["buffer_idx"])
            else: self.observations.append(doc.metadata["buffer_idx"])
            # dict_docs[keys[i]] = doc
        # self.memory_stream.update(dict_docs)
        self.get_memeory_stream()
        return keys

    async def aadd_documents(
        self, documents: List[Document], isThought = True, **kwargs: Any, 
    ) -> List[str]:
        """Add documents to vectorstore."""
        current_time = kwargs.get("current_time")
        if current_time is None:
            current_time = datetime.datetime.now()
        # Avoid mutating input documents
        dup_docs = [deepcopy(d) for d in documents]
        for i, doc in enumerate(dup_docs):
            if "last_accessed_at" not in doc.metadata:
                doc.metadata["last_accessed_at"] = current_time
            if "created_at" not in doc.metadata:
                doc.metadata["created_at"] = current_time
            if "started_at" not in doc.metadata:
                doc.metadata["started_at"] = self.retrieve_count
            if "hits" not in doc.metadata:
                doc.metadata["hits"] = 0
        keys = await self.vectorstore.aadd_documents(dup_docs, **kwargs)
        # dict_docs = {}
        for i, doc in enumerate(dup_docs):
            doc.metadata["buffer_idx"] = keys[i]
            if isThought: self.consciousness.append(doc.metadata["buffer_idx"])
            else: self.observations.append(doc.metadata["buffer_idx"])
        #     dict_docs[keys[i]] = {keys[i]: doc}
        # self.memory_stream.update(dict_docs)
        self.get_memeory_stream()
        return keys
    
    def remove_documents(self, documents: List[Document], **kwargs: Any) -> None:
        keys = [document['buffer_idx'] for document in documents]
        self.remove_documents_by_keys(keys, **kwargs)

    def remove_documents_by_keys(self, keys: List[str], **kwargs: Any) -> List[Document]:
        memory_stream = self.get_memeory_stream()
        poped_docs = []
        for key in keys:
            if key in self.consciousness: self.consciousness.remove(key)
            else: self.observations.remove(key)
            poped_docs.append(memory_stream[key])
        self.vectorstore.delete(keys)
        self.get_memeory_stream()
            
        return poped_docs
    
    def store(self, path):
        vectorstore_name = 'VectorDB'
        vectorstore_path = os.path.join(path, vectorstore_name)
        self.vectorstore.save_local(vectorstore_path)
        args = {}
        args.update(self.__dict__)
        args['vectorstore'] = vectorstore_name
        args.pop('memory_stream')
        jsonstr = json.dumps(args, ensure_ascii=False)
        with open(os.path.join(path, "arguments.json"),"w") as f:
            f.write(jsonstr+'\n')
        

    def init_from_checkpoint(self, path, embeddings):
        args_file = os.path.join(path,"arguments.json")
        if os.path.exists(args_file):
            with open(args_file, "r", encoding = 'utf-8') as f:
                args = json.load(f)
        vectorstore_path = os.path.join(path, args['vectorstore'])
        args['vectorstore'] = MyFAISS.load_local(vectorstore_path, embeddings)
        self.__dict__.update(args)
        self.get_memeory_stream()
        return self
        


