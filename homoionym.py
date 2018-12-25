from nltk.corpus import wordnet
from SPIMI import CleanData
from gensim.models import Word2Vec
import wikipedia

def homoionym(query):
    query = CleanData(query)
    wordsets = wordnet.synsets(query)
    homoionym_words = []
    for wordset in wordsets:
        words = wordset.lemma_names()
        homoionym_words.extend(words)
    return list(set(CleanData(" ".join(homoionym_words)).split()))

def BuildWordVector(sentences):
    model = Word2Vec(sentences, sg=1, size=30, window=5, min_count=3, negative=3, sample=0.001, hs=1, workers=4)
    model.save('Copurs.model')

def LoadWordVector(name="./model/w2v.model"):
    model = Word2Vec.load(name)
    return model

def W2v_Similarity(query, topn=5):
    model = LoadWordVector()
    similarwords = []
    if model.wv.__contains__(query):  # 查询扩展，导致效果下降，暂时不做修改,降低扩展词的权重
        similarwords = model.wv.most_similar(query, topn=topn)
    return similarwords

def Wiki_Similarity(query):
    similarwords = wikipedia.search(query)
    Wiki = []
    for phrase in similarwords:
        phrase = CleanData(phrase)
        phrase = phrase.split()
        Wiki.extend(phrase)
    return Wiki



if __name__ == '__main__':
    str = "liposarcoma"
    words = str.split()
    for word in words:
        print(Wiki_Similarity(word))