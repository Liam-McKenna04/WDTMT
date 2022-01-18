#Imports and constants 
import requests
import os
import snscrape.modules.twitter as sntwitter
import pandas as pd
import csv
USERNAME = 'pleasedshibe1'
NUMBER_OF_FOLLOWERS = 400
NUMBER_OF_TWEETS = 1000
MINFOLLOWERS = 0
MINTWEETS = 0
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFwVWwEAAAAAbbXaYfXjCrYkEvgAACKjs1j%2BMpM%3DQBBaL3UTuIxCIQs5LWkCjJM4CN2681q7lUX50PFfn0vm38UiKJ' 
#TODO: GET BEARER TOKEN FROM USER (twitter login)


#TODOS
# 1 USE PARALELLISM TO SPEED UP
# 2 IMPLIMENT CASHING
# 3 GET ONLY ENGLISH TWEETS/ACCOUNTS
# 4 GET RANDOM FOLLOWERS NOT IN ORDER 

def remove_none(initial_list: list):
    res = []
    for val in initial_list:
        if val != None:
            res.append(val)
    return res

def create_users_url(usernames: list):
    """Gets the user information of the usernames passed"""
    usernames_str = 'usernames=' + ','.join([str(elem) for elem in usernames])

    return "https://api.twitter.com/2/users/by?{}".format(usernames_str)

def get_params(user_fields=[], tweet_fields=[], max_value=0):
    
    return_dict = {"user.fields": ','.join([elem for elem in user_fields]),
            "tweet.fields" : ','.join(elem for elem in tweet_fields),
    }
    if max_value != 0:
        return_dict.update({'max_results': max_value})

    return return_dict

def bearer_oauth(r):

    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}" #TODO: GET TOKEN FROM CLIENT
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


#Gets id of the name entered 
users_url = create_users_url([USERNAME])
params = {'user.fields': 'id'}
json_response = connect_to_endpoint(users_url, params)
user_id = json_response['data'][0]['id']


#Gets followers names of user entered 
params = get_params(max_value=NUMBER_OF_FOLLOWERS)
followers_response = connect_to_endpoint("https://api.twitter.com/2/users/{}/followers".format(user_id), params,) #TODO: get more followers to sample (right now only 1000) #TODO: just get names

followers_username_list = []
for i in followers_response['data']:
    followers_username_list.append(i['username'])


#Gets data from sns

#create empty list to append full follower data 
df_mold = []
for follower_username in followers_username_list:
    print(follower_username)
    user_list = []
    # Creating list to append tweet data 
    # tweets_list1 = []

    #Using TwitterUserScraper to scrape user data for followers
    user = sntwitter.TwitterUserScraper(follower_username, False) #why won't profilescraper work
    user_object = user._get_entity()
    user_list = [user_object.username, user_object.displayname, (user_object.description).replace("\n", " "), user_object.statusesCount, user_object.followersCount, user_object.verified]

    if user_list[4] < MINFOLLOWERS and user_list[3] < MINTWEETS: # and protected is false: TODO # statusescount doesn't count retweets
        continue

    tweets_string = ""
    hashtags_used = []
    urls_used = []
    interacting_users = [] #potentially switch to retweets, mentioned users, and replys


    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(user.get_items()): #declare a username 
        if i>(NUMBER_OF_TWEETS - 1): #number of tweets you want to scrape
            break
        # tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username]) #declare the attributes to be returned
        tweets_string += (tweet.content + " ") #Potentially remove links/hashtags/@s from tweet content
        if tweet.inReplyToUser:
            interacting_users.append(tweet.inReplyToUser.username)
        if tweet.mentionedUsers:
            for user1 in tweet.mentionedUsers:
                interacting_users.append(user1.username)
        if tweet.retweetedTweet:
            interacting_users.append(tweet.retweetedTweet.user.username)
        if tweet.quotedTweet:
            interacting_users.append(tweet.quotedTweet.user.username)
        # if not tweet.retweetedTweet and not tweet.quotedTweet: #should i include hashtags from retweetedtweets
       
        hashtags_used.append(tweet.hashtags)
        urls_used.append(tweet.outlinks)
        

    tweets_string = tweets_string.replace("\n", " ")
    hashtags_used = remove_none(hashtags_used) #Optimize this
    urls_used = remove_none(urls_used)
    interacting_users = remove_none(interacting_users)



    tweets_string = ' '.join(x for x in tweets_string.split() if not x.startswith('http'))

    user_list.append(tweets_string)
    
    
    user_list.append(urls_used)
    user_list.append(hashtags_used)
    user_list.append(interacting_users)
    
    df_mold.append(user_list)

print("-"*40)
print('done')
print('-'*40)


with open(f"{USERNAME}.csv", 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(df_mold)

