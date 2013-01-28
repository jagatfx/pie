# Imports
from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import MP

import oauth2, urllib, urllib2, json

def home(request):
    return render_to_response('base.html', RequestContext(request))

def mp_detail(request, mp_name):
    mp = MP.objects.get(name=mp_name.replace('_', ' '))
    data = {"name": mp.name,
            "party": mp.party,
            "constituency": mp.constituency,
            "twitter": mp.twitter_handle}
    return render_to_response('mp.html', RequestContext(request, data))

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
        result.append(text.lower())
    return result

def tweet_tweeter(tweet):
    return tweet['user']['screen_name']

def json_decode(fn, *args):
    return json.loads(fn(*args))

### Twitter queries

def latest_tweets(mp_twitter="SamGyimah", num_tweets=5):
    """Returns a list of the most recent tweets by the MP. Each tweet is a dictionary."""
    def _helper():
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={0}&count={1}".format(mp_twitter, num_tweets)
        tweets = oauth_req(url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return json_decode(_helper)

def relevant_tweets(words):
    def _helper():
        url = "http://api.twitter.com/1.1/search/tweets.json"
        num_tweets = 100
        data = ' '.join(words)
        query = urllib.urlencode({'q':data, 'count':num_tweets})
        result = urllib2.urlopen(url, query)
        # tweets = oauth_req(url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        # print(tweets)
        print(result)
        return
        return tweets
    return json_decode(_helper)

def get_tweets(mp_name, mp_twitter=None):    
    """Returns tweets by the MP or about him."""
    def _get_mp_tweets():
        if mp_twitter:
            return tweet_text(latest_tweets(mp_twitter=mp_twitter, num_tweets=5))
    def _get_mentions():
        mentions = [mp_name]
        if mp_twitter: mentions.append("@"+mp_twitter)
        matches = relevant_tweets(mentions)
        not_by_mp = filter(lambda t: tweet_tweeter(t) != mp_twitter, matches)
        return tweet_text(not_by_mp)
    return _get_mp_tweets()# + _get_mentions()


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

# j = get_tweets("", "SamGyimah")
# k = keyword_filter(j, "")
# j = relevant_tweets('electionbot')
