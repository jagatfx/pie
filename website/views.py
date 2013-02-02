# Imports
# from django.template import RequestContext
# from django.shortcuts import render_to_response
# from website.models import MP

import os
import oauth2, urllib, urllib2, json

# os = pull TWITTER_* oauth tokens from environment
# oauth2 = to send secure authorized requests to the Twitter API
# urllib, urllib2 = parsing URL requests, etc.
# json = parsing JSON output from Twitter API

# def home(request):
#     mp_list = MP.objects.all()
#     data = {"mps": []}
#     for mp in mp_list:
#         mp_desc = {"name":mp.name, "url":mp.name.replace(" ", "_")}
#         data["mps"].append(mp_desc)

#     return render_to_response('index.html', RequestContext(request, data))

# def mp_detail(request, mp_name):
#     mp = MP.objects.get(name=mp_name.replace('_', ' '))
#     data = {"name": mp.name,
#             "image_url": "http://shreyaschand.com/img/mp/" + mp_name + ".png",
#             "party": mp.party,
#             "constituency": mp.constituency,
#             "twitter_handle": mp.twitter_handle,
#             "tweets": tweet_text(latest_tweets(mp.twitter_handle))}
#     return render_to_response('mp.html', RequestContext(request, data))

TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']

### Utility functions

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=""):
    consumer = oauth2.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key, secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content

def tweet_text(tweet_list):
    """Returns a list of the tweet's text from a list of tweets."""
    result = []
    for tweet in tweet_list:
        text = tweet["text"]
        result.append(text)
    return result

def tweet_tweeter(tweet):
    return tweet['user']['screen_name']

def safe(url):
    return urllib.quote(url, '/:-&?=')

def json_decode(fn, *args):
    return json.loads(fn(*args))

### Twitter queries

def latest_tweets(mp_twitter="SamGyimah", num_tweets=10):
    """Returns a list of the most recent tweets by the MP. Each tweet is a dictionary."""
    def _helper():
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={0}&count={1}".format(mp_twitter, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return json_decode(_helper)

def relevant_tweets(mp_name, mp_twitter='', num_tweets=100):
    """Returns a list of the most recent tweets about MP or @MP. Currently hacks together a list of tweets @MP and a list of tweets mentioning MP."""
    def _helper():
        url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&result_type=recent&count={1}".format(query, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    query = mp_name
    tweets = json_decode(_helper)
    at_tweets = []
    if mp_twitter:
        query = "to:"+mp_twitter
        at_tweets = json_decode(_helper)
    return tweets + at_tweets

def get_tweets(mp_name, mp_twitter=''):
    """Returns tweets by the MP or about him."""
    def _get_mp_tweets():
        if mp_twitter:
            return tweet_text(latest_tweets(mp_twitter=mp_twitter, num_tweets=5))
    def _get_mentions():
        matches = relevant_tweets(mp_name, mp_twitter)
        not_by_mp = filter(lambda t: tweet_tweeter(t) != mp_twitter, matches)
        return tweet_text(not_by_mp)
    return _get_mp_tweets() + _get_mentions()


### Analysis

# ALL_KEYWORDS = [t.title for t in Term.objects.all()]

def keyword_filter(text_list, keyword):
    # aliases = set("INSERT CODE HERE")
    aliases = set(["exactly", "referendum"])
    # Should this cut out the word matches as well in case a keyword is positive?
    return filter(lambda t: set(t.split(' ')) & aliases, text_list)

def analyze_sentiment(text_list, keyword):
    matched_tweets = keyword_filter(text_list, keyword)
    total_sentiment, num_tweets = 0, 0
    for match in matched_tweets:
        s = get_sentiment(match) ## Must write get_sentiment function
        if s:
            total_sentiment += s
            num_tweets += 1
    return (keyword, total_sentiment/num_tweets)

### Testing!

j = relevant_tweets('Sam Gyimah', 'SamGyimah')
k = j['statuses']
t = tweet_text(k)
