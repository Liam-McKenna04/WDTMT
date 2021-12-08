import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True).text
        }
        
        output.append(item)
        
    return output

def google_search(query):
    response = get_results(query)
    return parse_results(response)

searched_term = 'pleasedshibe'
print(searched_term)

searched_results = google_search(searched_term)
# print(searched_results)
for dict in searched_results:
    if 'twitch.tv' in dict['link']:
        print('twitch streamer') # add to list, printing for debugging purposes
    if 'youtube.com' in dict['link']: #TODO: and over certain theshold of subs, followers, etc
        print('youtube personality')
    if 'twitter.com' in dict['link']:
        print('twitter personality')
    if 'instagram.com' in dict['link']: 
        print('instagram personality')
    