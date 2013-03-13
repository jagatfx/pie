from string import ascii_letters

def extract_words(text):
    for char in text:
        if not char in ascii_letters:
            text = text.replace(char, ' ')
    return text.split()

def get_word_sentiment(word):
    return Sentiment.objects.get(word=word).value

def analyze_tweet_sentiment(tweet):
    words = extract_words(tweet)
    average = None
    total_value, i = 0, 0
    for word in words:
        word_sentiment = get_word_sentiment(word)
        if word_sentiment:
            total_value += word_sentiment
            i += 1
    if i:
        average = total_value / i
    return average
