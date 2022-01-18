import pandas as pd
import numpy as np
import math
from collections import Counter

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    if magA == 0 or magB == 0:
        return 0
    return dotprod / (magA * magB)


def counter_interacting_similarity(c1, c2, p1, p2):

    if p1 == p2:
        return 1
    if not bool(c1) or not bool(c2):
        return 0

    MUTUALS_CONSTANT = 7
    second_denom = len(list(c1.elements())) + len(list(c2.elements()))
    n1 = c1[p2]
    n2 = c2[p1]

    retweetedsim = counter_cosine_similarity(c1, c2)
    personalsim =  (n1 + n2) / second_denom
    final_val = ((retweetedsim * 1) + (personalsim * 1))/ 2 
    

    if final_val > 1:
        return 1
    return final_val   


def create_interacting_users_matrix(df1):
    interacting_row = []
    interacting_matrix = []
    for i, rowX in df1['interacting users'].iteritems():
        interacting_row = []
        for j, rowY in df1['interacting users'].iteritems():
            if type(rowY) == float or type(rowY) == float:
                interacting_row.append(1)
                continue
            counter1 = Counter(rowX)
            counter2 = Counter(rowY)
            interacting_row.append(counter_interacting_similarity(counter1, counter2, df1['username'].iloc[i], df1['username'].iloc[j]))
        interacting_matrix.append(interacting_row)
    return interacting_matrix


