import json
from nltk import FreqDist
import math
import os
from SPIMI import CleanData
import time
import xmlprase
import csvprase
from homoionym import homoionym
from gensim.models import Word2Vec


def BM25(dic, querys='', k1=2, k3=1, b=0.75, cleanq=True):
    print("*******************************************")
    start = time.thread_time()
    N = 241006  # 文档总数
    avg_l = 300  # 平均文档长度
    # 可改进倒排索引合并策略
    if cleanq:
        querys = CleanData(querys)
    querys = querys.split()
    qtf_ = FreqDist(querys)  # 查询中的词频分布
    bm25 = {}
    model = Word2Vec.load("./model/Copurs.model")  #模型训练了数据集的词向量
    for query in querys:
        raw_query = query   #保存原始查询
        if model.wv.__contains__(query):    #查询扩展，导致效果下降，暂时不做修改,降低扩展词的权重
            homoionyms = model.wv.most_similar(query, topn=5)
            homo_query = [CleanData(e[0]) for e in homoionyms]
            homo_query.append(query)
        else:
            homo_query = [query]
        # print("word2vec 得到的近义词是：", homoionyms)
        for sim_query in homo_query:  # 查询扩展
            query = sim_query
            if query not in dic:
                continue
            docs = dic[query]
            df = len(docs)
            qtf = qtf_[raw_query]
            for doc in docs:
                doc = doc.split()
                tf = float(doc[1])
                ld = float(doc[2])
                W = qtf / (k3 + qtf) * (k1 + tf) / (tf + k1 * (1 - b + b * ld / avg_l)) * math.log2(
                    (N - df + 0.5) / (df + 0.5))
                if sim_query!=raw_query:
                    if doc[0] in bm25:
                        bm25[doc[0]] += W
                    else:
                        bm25[doc[0]] = W
                else:
                    if doc[0] in bm25:
                        bm25[doc[0]] += W*5
                    else:
                        bm25[doc[0]] = W*5
    w_qd = sorted(bm25.items(), key=lambda x: x[1], reverse=True)
    end = time.thread_time()
    print("一共查询到", len(w_qd), "个结果,用时", end - start, "s")
    # print("检索结果：", w_qd)
    return bm25, w_qd


def Fulltext_search(dic, query=''):
    return BM25(dic, query)


def Level_search(dic, dic_level, query=''):
    bm25, w_qd = BM25(dic_level, query)
    if len(bm25) < 100:
        bm25_, w_qd_ = BM25(dic, query)
        bm25.update(bm25_)
    return bm25, w_qd


def LoadInvertable():
    path = os.getcwd()
    Invertable = path + "\clinicallevel_cleaned_txt.json"
    with open(Invertable, "r", encoding="utf-8") as fr:
        file = fr.read()
        fr.close()
    dic_level = json.loads(file)
    dic = dic_level
    print("finished loading invertable!")
    return dic, dic_level

def JudgeProcess(k):
    count = 0
    for j in range(k):
        if w_qd[j][0] in judgement[str(i + 1)]:
            count += 1
    print("p@", k, ":", count / k)


if __name__ == '__main__':
    dic, dic_level = LoadInvertable()
    topics = xmlprase.parsexml()
    judgement = csvprase.prasecsv()
    for (i, query) in enumerate(topics):
        # bm25, w_qd = Fulltext_search(dic, query)
        bm25, w_qd = Level_search(dic, dic_level, query)
        for k in [5, 10, 15]:
            JudgeProcess(k)
