# Imports
from sentiment import analyze_tweet_sentiment
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

def tweets_by(mp_twitter, num_tweets=10):
    """Returns a list of the most recent tweets by the MP. Each tweet is a dictionary."""
    def _api_helper():
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={0}&count={1}".format(mp_twitter, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return parse_tweets(json.loads(_api_helper()))

def tweets_at(mp_twitter, num_tweets=10):
    """Returns a list of the most recent tweets @MP."""
    def _api_helper():
        url = "https://api.twitter.com/1.1/search/tweets.json?q=to:{0}&result_type=recent&count={1}".format(mp_twitter, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return parse_tweets(json.loads(_api_helper())['statuses'])

def tweets_all(num_tweets=10):
    def _api_helper():
        url = "https://api.twitter.com/1.1/lists/statuses.json?list_id=86633145&count={0}".format(num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return parse_tweets(json.loads(_api_helper()))

## UNUSED ##
def mentioned_tweets(mp_name, num_tweets=100):
    def _api_helper():
        url = "https://api.twitter.com/1.1/search/tweets.json?q={0}&result_type=recent&count={1}".format(mp_name, num_tweets)
        safe_url = safe(url)
        tweets = oauth_req(safe_url, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweets
    return parse_tweets(json.loads(_api_helper())['statuses'])

def relevant_tweets(mp_name, mp_twitter='', num_tweets=100, only_at=False):
    """Returns a list of the most recent tweets about MP or @MP. Currently hacks together a list of tweets @MP and a list of tweets mentioning MP."""
    if mp_twitter:
        tweets_at = tweets_at(mp_twitter)
    mentions = mentioned_tweets(mp_name)
    return mentions + tweets_at

def get_tweets(mp_name, mp_twitter=''):
    """Returns tweets by the MP or about him. Should only be used for data analysis."""
    all_tweets = []
    if mp_twitter:
        all_tweets += parse_tweets(tweets_by(mp_twitter))
    matches = relevant_tweets(mp_name, mp_twitter)
    not_by_mp = filter(lambda t: t['user']['screen_name'] != mp_twitter, matches)
    all_tweets += parse_tweets(not_by_mp)
    return all_tweets

### Utility functions

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=""):
    consumer = oauth2.Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key, secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content

def parse_tweets(tweet_list):
    """Returns a dict with keys 'from', 'content', and 'date'."""
    def tweet_date(tweet):
        data = tweet["created_at"].split()
        month, day, year = data[1], data[2], data[-1]
        time = data[3][:-3] # currently returns as 24-hr time, hh:mm
        return "{0}, {1} {2}, {3}".format(time, month, day, year)
    try:
        result = []
        for t in tweet_list:
            tweet_dict = {'from':linkify_tweet('@'+t['user']['screen_name']),
                          'content':linkify_tweet(t['text']),
                          'date':tweet_date(t)}
            sent = analyze_tweet_sentiment(t['text'])

            if sent > 0:
                sent = '<span class="positive">' + str(sent)[:4]
            elif sent < 0:
                sent = '<span class="negative">' + str(sent)[:5]
            else:
                sent = '<span class="muted">' + str(sent)
            tweet_dict['sentiment'] = sent + '</span>'

            result.append(tweet_dict)

        return result
    except TypeError as e:
        return [{'content':'', 'from':'', 'date':''}]

def safe(url):
    return urllib.quote(url, '/:-&?=')

def linkify_tweet(tweet):
    '''Add links to twitter tweets.'''
    def wrapall(word_list, cond, proc):
        '''Wrap words given a condition func and processing func'''
        return map(lambda x: proc(x) if cond(x) else x, word_list)
    def hashify(term):
        a = u'<a href="https://twitter.com/search/realtime?q=%23{0}&src=hash" target="_blank">'
        return a.format(term[1:]) + term + u'</a>'
    def atify(term):
        a = u'<a href="https://twitter.com/{}" target="_blank">{}</a>'
        return a.format(term, term)
    def linkify(term):
        a = u'<a href="{}" target="_blank">{}</a>'
        return a.format(term, term)
    words = tweet.split()
    words = wrapall(words, lambda x: x[0] == '#', hashify)
    words = wrapall(words, lambda x: x[0] == '@', atify)
    # words = wrapall(words, lambda x: x[:len('http')] == 'http', linkify) # disabled for security reasons
    return ' '.join(words)
