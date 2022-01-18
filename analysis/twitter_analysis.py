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
import pickle
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from text_analysis_module import pr1
from text_analysis_module import pr2
from text_analysis_module import create_text_matrix
from hashtag_analysis_module import create_hashtag_matrix
from interacting_user_analysis_module import create_interacting_users_matrix


USERNAME = 'pleasedshibe1' #TODO: Get from front end
header = ['username', 'name', 'description', 'number of tweets', 'followers', 'verified', 'tweets', 'links', 'hashtags', 'interacting users']
df1 = pd.read_csv(f"{USERNAME}.csv", header=None, names=header, index_col=False) #TODO: Get column directly from query


def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


df1 = df1[df1['tweets'].notna()]
df1.reset_index(drop=True, inplace=True)


#1 Text similarity
df1 = df1[df1['tweets'].notna()]
# df1 = df1[df1['interacting users'].notna()]
df1.reset_index(drop=True, inplace=True)


text_matrix = create_text_matrix(df1)
hashtag_matrix = create_hashtag_matrix(df1)
interacting_users_matrix = create_interacting_users_matrix(df1)


print(len(interacting_users_matrix), 'by', len(interacting_users_matrix[0]))
print(len(hashtag_matrix), 'by', len(hashtag_matrix[0]))
print(len(text_matrix), 'by', len(text_matrix[0]))
text_mtx = np.matrix(text_matrix)
hashtag_mtx = np.matrix(hashtag_matrix)
interact_mtx = np.matrix(interacting_users_matrix)

similarity_matrix = (0 * text_mtx) + (0 * hashtag_mtx) + (1 * interact_mtx)
np.save(f'{USERNAME}_similarity_matrix.npy', similarity_matrix)
np.save('text_mtx.npy', text_mtx)
np.save('hashtag_mtx.npy', hashtag_mtx)
np.save('interact_mtx.npy', interact_mtx)

df1.to_csv(f'{USERNAME}finished.csv')