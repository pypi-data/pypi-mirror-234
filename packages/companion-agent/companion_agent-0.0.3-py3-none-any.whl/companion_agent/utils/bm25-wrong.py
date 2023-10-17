import numpy as np
from collections import Counter
import jieba


class BM25_Model(object):
    def __init__(self, documents_list, k1=2, k2=1, b=0.5):
        documents_list = [list(jieba.cut(doc)) for doc in documents_list]
        self.documents_list = documents_list
        self.documents_number = len(documents_list)
        self.avg_documents_len = sum([len(document) for document in documents_list]) / self.documents_number
        self.f = []
        self.idf = {}
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.init()

    def init(self):
        df = {}
        for document in self.documents_list:
            temp = {}
            for word in document:
                temp[word] = temp.get(word, 0) + 1
            self.f.append(temp)
            for key in temp.keys():
                df[key] = df.get(key, 0) + 1
        for key, value in df.items():
            self.idf[key] = np.log((self.documents_number - value + 0.5) / (value + 0.5))

    def get_score(self, index, query):
        score = 0.0
        document_len = len(self.f[index])
        qf = Counter(query)
        for q in query:
            if q not in self.f[index]:
                continue
            score += self.idf[q] * (self.f[index][q] * (self.k1 + 1) / (
                        self.f[index][q] + self.k1 * (1 - self.b + self.b * document_len / self.avg_documents_len))) * (
                                 qf[q] * (self.k2 + 1) / (qf[q] + self.k2))
        return score

    def get_documents_score(self, query):
        query = list(jieba.cut(query))
        score_list = []
        for i in range(self.documents_number):
            score_list.append(self.get_score(i, query))
        score_list = [(score, step) for step, score in enumerate(score_list)]
        score_list.sort(key=lambda x: x[0], reverse=True)
        score_list = [(*score, step) for step, score in enumerate(score_list)]
        score_list.sort(key=lambda x: x[1])
        sort_list = np.array(score_list)

        def _l2_norm(x):
            x -= x.min()
            l2 = np.linalg.norm(x)
            return x / (0.01 if not l2 else l2)

        def _min_max_norm(x):
            x -= x.min()
            x /= x.max()
        
        _min_max_norm(sort_list[:,0])
        return sort_list.tolist()
    

def faiss_test(query, documents_list):
    from langchain.embeddings.openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    import faiss
    index = faiss.IndexFlatL2(1536)

    def add(vec):
        vector = np.array(vec, dtype=np.float32)
        faiss.normalize_L2(vector)
        index.add(vector)

    documents_list = embeddings.embed_documents(documents_list+[query])
    query = documents_list.pop(-1)
    add(documents_list)

    query = np.array([query], dtype=np.float32)
    # faiss.normalize_L2(query)
    scores, indices = index.search(query, len(documents_list))
    sort_list = list(zip(scores[0], indices[0], range(len(scores[0]))))
    sort_list.sort(key=lambda x: x[1])
    sort_list = np.array(sort_list)
    return sort_list.tolist()
    



# dialogs = ["包龙星说：“将军！”",
#             "爷爷说：“恩恩……”",
#             "包龙星说：“我飞帅再将。”",
#             "爷爷说：“你飞帅，我就吃你的帅。”",
#             "包龙星说：“啊……哎呀……”",
#             "爷爷说：“你不要以为当了官就很威风。”",
#             "包龙星说：“我那比得上你？”",
#             "爷爷说：“你还记不记的我告诉过你，当官呢要清如水，廉如镜。”",
#             "包龙星说：“爹，听说你以前都是……”",
#             "爷爷说：“没错，我以前是个贪官。我诨名叫“弯了能弄直，死了能救活”，就是因为我做了太多缺德事，所以你十二个哥哥没有一个养得活，害得我每年白发人送黑发人。最后没有办法，我唯有告老还乡，把家产全捐出去做善事，就这样，才保住你这一条小命呀儿子。（转身回屋）你看，我给你写了个字挂在中堂上，就是这个廉洁的“廉”字。”",
#             "包龙星说：“我怎么看，它分明都像个……贪字。”"]

# bm25_model = BM25_Model(dialogs)

# query = "“爹，我字忘拿了”"
# scores_openai = faiss_test(query, dialogs)
# scores_bm25 = bm25_model.get_documents_score(query)
# for a, b, c in zip(scores_openai, scores_bm25, dialogs):
#     print(f"{int(a[-1])}    {int(b[-1])}    {c}")