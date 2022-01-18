
from gensim.matutils import jensen_shannon

import pandas as pd
import numpy as np

import json
import glob

#Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel


#spacy
import spacy
from nltk.corpus import stopwords

#vis
import pyLDAvis
import pyLDAvis.gensim_models as gensim_models
import warnings
from gensim.models import TfidfModel
from collections import Counter
import pickle



def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB"]):
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    texts_out = []
    for text in texts:
        doc = nlp(text)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return (texts_out)

def gen_words(texts):
    final = []
    for text in texts:
        new = gensim.utils.simple_preprocess(text, deacc=True)
        final.append(new)
    return final

stop_words = stopwords.words('english')

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def pr1(df1):
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'get', 'lol', 'let', 'get', 'dm', ])

    lemmatized_texts = lemmatization(df1['tweets'])
    data_words = gen_words(lemmatized_texts)


    data_words_nostops = remove_stopwords(data_words)
    data_words =  [[word for word in doc if len(word) > 2] for doc in data_words_nostops]


    #BIGRAMS AND TRIGRAMS
    
    bigram_phrases = gensim.models.Phrases(data_words, min_count=6, threshold=50)
    trigram_phrases = gensim.models.Phrases(bigram_phrases[data_words], threshold=50)

    bigram = gensim.models.phrases.Phraser(bigram_phrases)
    trigram = gensim.models.phrases.Phraser(trigram_phrases)

    def make_bigrams(texts):
        return([bigram[doc] for doc in texts])

    def make_trigrams(texts):
        return ([trigram[bigram[doc]] for doc in texts])

    data_bigrams = make_bigrams(data_words)
    data_bigrams_trigrams = make_trigrams(data_bigrams)


    id2word = corpora.Dictionary(data_bigrams_trigrams)
    texts = data_bigrams_trigrams

    corpus = [id2word.doc2bow(text) for text in texts]
    tfidf = TfidfModel(corpus, id2word=id2word)
    low_value = 0.4 #TODO: AUTOTUNE HYPERPERAMETERS
    #TODO: LDAMULTICORE
    words = []
    words_missing_in_tfidf = []
    for i in range(0, len(corpus)):
        bow = corpus[i]
        low_value_words = []
        tfidf_ids = [id for id, value in tfidf[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf[bow] if value < low_value]
        drops = low_value_words+words_missing_in_tfidf
        for item in drops:
            words.append(id2word[item])
        words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids]

        new_bow = [b for b in bow if b[0] not in low_value_words and b[0]not in words_missing_in_tfidf]
        corpus[i] = new_bow
    
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=8, 
                                                random_state=100,
                                                chunksize=100,
                                                passes=10,
                                                alpha=0.01,
                                                eta=0.9)    
    lda_model.save('lda.model')
    with open('corpus.ob', 'wb') as fp:
        pickle.dump(corpus, fp)
    return lda_model, corpus



def pr2(model, corpus, df1):
    
    text_row = []
    difference_matrix = [] 
    for ii in range(len(df1)):
        text_row = []
        Xvec = model.get_document_topics(corpus[ii], minimum_probability=0)
        for jj in range(len(df1)):
            Yvec = model.get_document_topics(corpus[jj], minimum_probability=0)
            text_row.append(1 - jensen_shannon(Xvec, Yvec))
        difference_matrix.append(text_row)    
    return difference_matrix

def create_text_matrix(df):
    model, corpus1 = pr1(df)
    difference_matrix = pr2(model=model, corpus=corpus1, df1=df)
    return difference_matrix