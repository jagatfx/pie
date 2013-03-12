# Imports
import os
import oauth2, urllib, urllib2, json

# os = pull TWITTER_* oauth tokens from environment
# oauth2 = to send secure authorized requests to the Twitter API
# urllib, urllib2 = parsing URL requests, etc.
# json = parsing JSON output from Twitter API

TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']

### Twitter queries

def latest_tweets(mp_twitter="SamGyimah", num_tweets=10):
    """Returns a list of the most recent tweets by the MP. Each tweet is a dictionary."""
    def _api_helper():
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={0}&count={1}".format(mp_twitter, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return json_decode(_api_helper)

def at_tweets(mp_twitter, num_tweets=100):
    """Returns a list of the most recent tweets @MP."""
    def _api_helper():
        url = "https://api.twitter.com/1.1/search/tweets.json?q=to:{0}&result_type=recent&count={1}".format(mp_twitter, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return json_decode(_api_helper)['statuses']

def mentioned_tweets(mp_name, num_tweets=100):
    def _api_helper():
        url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&result_type=recent&count={1}".format(mp_name, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return json_decode(_api_helper)['statuses']

def relevant_tweets(mp_name, mp_twitter='', num_tweets=100, only_at=False):
    """Returns a list of the most recent tweets about MP or @MP. Currently hacks together a list of tweets @MP and a list of tweets mentioning MP."""
    if mp_twitter:
        at_tweets = at_tweets(mp_twitter)
    mentions = mentioned_tweets(mp_name)
    return mentions + at_tweets

def get_tweets(mp_name, mp_twitter=''):
    """Returns tweets by the MP or about him. Should only be used for data analysis."""
    all_tweets = []
    if mp_twitter:
        all_tweets += parse_tweet(latest_tweets(mp_twitter=mp_twitter, num_tweets=10))
    matches = relevant_tweets(mp_name, mp_twitter)
    not_by_mp = filter(lambda t: t['user']['screen_name'] != mp_twitter, matches)
    all_tweets += parse_tweet(not_by_mp)
    return all_tweets

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

### Utility functions

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=""):
    consumer = oauth2.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key, secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content

def parse_tweet(tweet_list):
    """Currently returns a list of "text - sent date" strings."""
    # print tweet_list[0]
    def tweet_date(tweet):
        data = tweet["created_at"].split()
        month, day, year = data[1], data[2], data[-1]
        time = data[3][:-3] # currently returns as 24-hr time, hh:mm
        return "{0}, {1} {2}, {3}".format(time, month, day, year)
    try:
        return [linkify_tweet(u'@{0}: {1} - sent {2}'.format(t["user"]["screen_name"], t["text"], tweet_date(t))) for t in tweet_list]
    except TypeError as e:
        return ["Sorry, we are unable to access these tweets. Perhaps they are protected."]

def safe(url):
    return urllib.quote(url, '/:-&?=')

def json_decode(fn, *args):
    return json.loads(fn(*args))

def linkify_tweet(tweet):
    '''Add links to twitter tweets.'''
    def wrapall(word_list, cond, proc):
        '''Wrap words given a condition func and processing func'''
        return map(lambda x: proc(x) if cond(x) else x, word_list)
    def hashify(term):
        a = '<a href="https://twitter.com/search/realtime?q=%23{0}&src=hash" target="_blank">'
        return a.format(term[1:]) + term + '</a>'
    def atify(term):
        a = '<a href="https://twitter.com/{}" target="_blank">{}</a>'
        return a.format(term, term)
    def linkify(term):
        a = '<a href="{}" target="_blank">{}</a>'
        return a.format(term, term)
    words = tweet.split()
    words = wrapall(words, lambda x: x[0] == '#', hashify)
    words = wrapall(words, lambda x: x[0] == '@', atify)
    # words = wrapall(words, lambda x: x[:len('http')] == 'http', linkify) # disabled for security reasons
    return ' '.join(words)
