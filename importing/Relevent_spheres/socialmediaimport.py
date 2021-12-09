import pandas as pd
import numpy as np
import requests
import random
import string
import praw
import pprint
search_query = 'IPhone11'


code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

#Reddit
reddit_dicts = []
reddit_public_key = "oabULyw3WZYI3r1psex8Qg"
reddit_secret_key = "m_fFaIoCNW3IufIYcksfu46P_lGLVg"
r = praw.Reddit(client_id=reddit_public_key, client_secret=reddit_secret_key, user_agent='Clustering bot v0.0.1 by u/SplitShadow')
page = r.subreddit('all')
posts = page.search('ludwig', limit=25)
count = 0

for post in posts:
    if count == 0:
        print(post.title)
        # pprint.pprint(vars(post))
    count += 1
    reddit_dicts.append({   'title': post.title,
                            'text': post.selftext,
                            'likes': post.score,
                            'subreddit': post.subreddit_name_prefixed,
                            'author': post.author.name,
                            'num_comments': post.num_comments,
                            #TODO: ADD COMMENTS AND COMMENT AUTHORS AS ADDITIONAL POSTS WITH COMMENT FIELD ON



    })
print(reddit_dicts)
#Twitter
twitter_public_key = 'zJ9SuHAxrbRSn3j4NtegblSds'
twitter_secret_key = '6jUqoqNtx9kgoLFEZ4ULcqiU68D2m5m0UHiYsHAtEISpgGjNf2'
Ttoken = 'AAAAAAAAAAAAAAAAAAAAAFwVWwEAAAAANzh8iPObylRH4opzfC5yygZX9Oo%3DkIQFb1HtNr51XMfDMZgF2SanYBhuqhBXRXhRXz8RJxqKdwimE7'
Tauth = tweepy.OAuthHandler(twitter_public_key, twitter_secret_key)
Tauth.set_access_token(Ttoken)
Tapi = tweepy.API(auth)
public_tweets = Tapi.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


#Youtube 

#general search

