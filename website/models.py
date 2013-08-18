from django.db import models

# Create your models here.
MAX_TWEET_LENGTH = 140
TWITTER_HANDLE_MAX_LEN = 30

class Politico(models.Model):
    POLITICO_TYPES = (
        ('MP', 'MP'),
        ('LD', 'Lord'),
    )
    class Meta:
        verbose_name = u'Politico'
        verbose_name_plural = u'Politicos'
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=2, choices=POLITICO_TYPES)
    party = models.CharField(max_length=30)
    constituency = models.CharField(max_length=30)
    twitter_handle = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Media(models.Model):
    class Meta:
        verbose_name = u'Media Personality'
        verbose_name_plural = u'Media Personalities'
    name = models.CharField(max_length=30)
    party_leaning = models.CharField(max_length=30)
    affiliation = models.CharField(max_length=30)
    twitter_handle = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Term(models.Model):
    class Meta:
        verbose_name = u'Term'
        verbose_name_plural = u'Terms'
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

class TermAlias(models.Model):
    class Meta:
        verbose_name = u'Term Alias'
        verbose_name_plural = u'Term Aliases'
    term = models.ForeignKey('Term')
    alias = models.CharField(max_length=30)

    def __unicode__(self):
        return self.term.title + ': ' + self.alias

class Sentiment(models.Model):
    word = models.CharField(max_length=75)
    value = models.FloatField()

    def __unicode__(self):
        return self.word + u': ' + str(self.value)

class Tweet(models.Model):
    author = models.ForeignKey(Politico)
    author = models.CharField(max_length=TWITTER_HANDLE_MAX_LEN)
    recipient = models.CharField(max_length=TWITTER_HANDLE_MAX_LEN) # allow Null. NULL = not at anyone
    body = models.TextField(max_length=MAX_TWEET_LENGTH)

class HashTag(models.Model):
    tag = models.CharField(max_length=MAX_TWEET_LENGTH)
    tweet = models.ManyToManyField(Tweet)

