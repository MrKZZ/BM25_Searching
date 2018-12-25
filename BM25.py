import json
from nltk import FreqDist
import math
import os
from SPIMI import CleanData
import time
import xmlprase
import csvprase
from homoionym import W2v_Similarity, Wiki_Similarity
from Mesh import Mesh

def BM25(dic, querys):
    print("*******************************************")
    start = time.thread_time()
    # 可改进倒排索引合并策略
    query_list = []
    for _,value in querys.items():
        value = value.split()
        query_list.extend(value)
    qtf_ = FreqDist(query_list)  # 查询中的词频分布
    bm25 = {}
    homo_query = []
    homo_query1 = []
    homo_query2 = []
    homo_query3 = []
    #这里控制不同查询项权重
    for key,query in querys.items():
        temp = query.split()
        for query in temp:
            if key == 0:
                homoionyms = W2v_Similarity(query, 5)
                homo_query2 += [CleanData(e[0]) for e in homoionyms]
                homo_query3 += [CleanData(e[0]) for e in Mesh(query)]
            if key != 2:
                homo_query1 += Wiki_Similarity(query)
    # #
    # # #合并查询扩展
    homo_query += homo_query2 + homo_query2 + homo_query3
    bm25 = calculate_bm25(dic, homo_query, bm25)
    bm25 = calculate_bm25_(dic, querys, bm25, qtf_=qtf_, weight_=len(homo_query))
    # bm25 = calculate_bm25_(dic, querys, bm25, qtf_=qtf_, weight_=5)
    w_qd = sorted(bm25.items(), key=lambda x: x[1], reverse=True)
    end = time.thread_time()
    print("一共查询到", len(w_qd), "个结果,用时", end - start, "s")
    return bm25, w_qd

def calculate_bm25(dic, query, bm25, k1=2, k3=1, b=0.75,):
    N = 241006  # 文档总数
    avg_l = 300  # 平均文档长度
    for sim_query in query:
            query = sim_query
            if query not in dic:
                continue
            docs = dic[query]
            df = len(docs)
            qtf = 0.8
            for doc in docs:
                doc = doc.split()
                tf = float(doc[1])
                ld = float(doc[2])
                W = qtf / (k3 + qtf) * (k1 + tf) / (tf + k1 * (1 - b + b * ld / avg_l)) * math.log2(
                    (N - df + 0.5) / (df + 0.5))
                if doc[0] in bm25:
                    bm25[doc[0]] += W
                else:
                    bm25[doc[0]] = W
    return bm25

def calculate_bm25_(dic, querys, bm25, qtf_, weight_, k1=2, k3=1, b=0.75,):
    N = 241006  # 文档总数
    avg_l = 300  # 平均文档长度
    for key,value in querys.items():
        temp = value.split()
        for query in temp:
            if query not in dic:
                continue
            docs = dic[query]
            df = len(docs)
            qtf = qtf_[query]
            for doc in docs:
                doc = doc.split()
                tf = float(doc[1])
                ld = float(doc[2])
                W = qtf / (k3 + qtf) * (k1 + tf) / (tf + k1 * (1 - b + b * ld / avg_l)) * math.log2(
                    (N - df + 0.5) / (df + 0.5))
                weight = weight_ - key
                if doc[0] in bm25:
                    bm25[doc[0]] += W * weight
                else:
                    bm25[doc[0]] = W * weight
    return bm25

def Query_Extend():
    with open("Medical Words.txt", "r", encoding="utf-8") as fr:
        file = fr.readlines()
    extend_querys = []
    for line in file:
        line = CleanData(line)
        extend_querys.append(line)
    return extend_querys


def Fulltext_search(dic, query):
    return BM25(dic, query)


def Level_search(dic, dic_level, query):
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
        results = judgement[str( i+1 )].split()
        if "NCT0" + w_qd[j][0] in results[:]:
            print("NCT0"+w_qd[j][0], results.index("NCT0"+w_qd[j][0]))
            count += 1
    print("p@", k, ":", count / k)


def eval_res(res, eval_path, query_id):
    '''
    评估结果，并将结果写入文件
    Args:
    res tuple 查询结果
    res_path str 结果存储文件
    '''
    res_list = []
    print(len(res))
    for i, query_res in enumerate(res):
        doc_id = query_res[0]
        score = query_res[1]
        res_list.append(str(query_id + 1) + " Q0 " + "NCT0" + str(doc_id) + " " + str(i+1) + " " + str(score) + " myrun"+'\n')

    with open(eval_path, 'a', encoding="utf-8") as fw:
        for e in res_list:
            fw.write(e)


if __name__ == '__main__':
    dic, dic_level = LoadInvertable()
    #topics, weights = xmlprase.parsexml()
    topics = xmlprase.parsexml1()
    judgement = csvprase.prasecsv()
    for i,query in enumerate(topics):
        bm25, w_qd = Level_search(dic, dic_level, query)
        eval_res(w_qd[:15], "out123.txt", i)
        print(w_qd[:15])
        # for k in [5, 10, 15]:
        #     JudgeProcess(k)