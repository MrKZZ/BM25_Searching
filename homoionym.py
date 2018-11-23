from nltk.corpus import wordnet
from SPIMI import CleanData
from gensim.models import Word2Vec

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

def LoadWordVector(name='Copurs.model'):
    model = Word2Vec.load(name)
    return model

def Similarity(query):
    model = LoadWordVector()
    similarwords = model.most_similar(query)
    return similarwords
