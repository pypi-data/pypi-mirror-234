"""Wrapper around FAISS vector database."""
from langchain import FAISS

from typing import Any

import numpy as np

class MyFAISS(FAISS):

    def delete(self, ids = [], **kwargs: Any):
        index_list = []
        # print(self.index_to_docstore_id)
        docstore_id_to_index = {v:k for k,v in self.index_to_docstore_id.items()}
        for id in ids:
            index = docstore_id_to_index[id]
            index_list += [index]
            self.docstore._dict.pop(id)
            docstore_id_to_index.pop(id)
        self.index.remove_ids(np.array(index_list))
        # print(docstore_id_to_index)
        docstore_id_to_index = sorted(docstore_id_to_index.items(), key=lambda x:x[1])
        # print(docstore_id_to_index)
        self.index_to_docstore_id = {i:item[0] for i,item in enumerate(docstore_id_to_index)}