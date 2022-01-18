import pandas as pd
import numpy as np
from collections import Counter
import math
from ast import literal_eval



def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i



def counter_cosine_similarity(c1, c2):
    
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    if magA == 0 or magB == 0:
        return 0
    return dotprod / (magA * magB)




def create_hashtag_matrix(df1):

    hashtag_row = []
    hashtag_matrix = []

    df1['hashtags'] = df1.hashtags.apply(lambda x: literal_eval(str(x)))
    for i in range(len(df1)):
        df1['hashtags'].iloc[i] = list(flatten(df1['hashtags'].iloc[i]))
    
    for i, rowX in df1['hashtags'].iteritems():
        hashtag_row = []
        for j, rowY in df1['hashtags'].iteritems():
            if i == j:
                hashtag_row.append(1)
                continue
            counterA = Counter(rowX) # make sure counter considers amount 
            counterB = Counter(rowY)
            hashtag_row.append(counter_cosine_similarity(counterA, counterB))
        hashtag_matrix.append(hashtag_row)
    return hashtag_matrix
    
