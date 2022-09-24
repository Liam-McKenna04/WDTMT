# Abstract
WDTMT, or sphere, is a personal project to show the nuances and the intracies of a twitter following using data science techniques and python. I originally intended to just analyze the data, but I ended up using NLP to get a better grasp of tweets and clustering algorighms to group followings into niches. 
# How it works
## Importing
Sphere utilizes the twitter API and snscrape to make importing data cheap and easy. This was the most efficient method I could find without breaking the bank. 
## Basic analysis and drawing connections
### 1. Textual analysis and tokenization
Textual analysis is done through a process of cleaning the data (lemmization, removing stopwords), altering the data (making bigrams and trigrams), and finally utilising gensim to create a lda model and making a difference matrix. 
### 2. General analysis
Analysis is done on hashtags, interactions, and similar text in tweets. These comparisons are done by utilizing counter cosine similarity between two different users. 
## Displaying connections
### 1. Displaying clusters using an Intertopic Distance Map
This model clearly shows the overlap between many groups of a follow base, theres usually only a few terms/relationships/etc. that stick out
#### 1a. Displaying clusters using an Intertopic Distance Map that only depends on textual analysis
It is apparent that when ignoring hashtags and related infollows, the analysis of a follower base becomes much harder and the data becomes much more spread out. We can conclude that even if individuals follow many of the same users, they often tweet about unique things. 
### 2. Displaying clusters using an Overlap Computing Function 
This function more clearly weighs infollows, or followers following eachother. This graph shows us that followers typically belong to niches or cliques, and it is usual for these niches to have a mini-figurehead of their own, which most of the followers also follow.
# Todo and future progress
- Define clusters 
- Do sentiment analysis on individual clusters 
