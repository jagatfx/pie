from django.db import models

# Create your models here.

class MP(models.Model):
    class Meta:
        verbose_name = u'MP'
        verbose_name_plural = u'MP\'s'
    name = models.CharField(max_length=30)
    party = models.CharField(max_length=30) 
    constituency = models.CharField(max_length=30)
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
