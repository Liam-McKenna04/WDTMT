import tweepy
import requests
import json

consumer_key = 'JH0ncxZihoak2jEPAKzSlkmbD'
consumer_secret = 'ESmnoFt0USjzwmwc39doupHYDIeG53ijIieT93YcTMzAqbklK7'
Ttoken = '1450174048336556037-fGC06TJ9QKgBkHR4xCP3ituG2DXhdh'
Ttoken_secret = '5jdMfqV3zykbyXWlvYovuF8RgXapQBJgoBQTxWmbBEN0z'
Btoken = 'AAAAAAAAAAAAAAAAAAAAAFwVWwEAAAAAbbXaYfXjCrYkEvgAACKjs1j%2BMpM%3DQBBaL3UTuIxCIQs5LWkCjJM4CN2681q7lUX50PFfn0vm38UiKJ'

def search_twitter(query, tweet_fields, max_results, bearer_token = 'BEARER_TOKEN'):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&max_results={}&{}".format(
        query, max_results, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

query = 'Drake'
tweet_fields = 'tweet.fields=id,text,author_id,created_at,in_reply_to_user_id,lang,referenced_tweets' #GET INFO ABOUT AUTHOR ID AND ADD WHEN CONVERTING TO DF
json_response = search_twitter(query=query, max_results=50, tweet_fields=tweet_fields, bearer_token=Btoken)
print(json.dumps(json_response, indent=4, sort_keys=True))

