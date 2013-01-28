from django.db import models

# Create your models here.

class MP(models.Model):
    class Meta:
        verbose_name = "MP"
        verbose_name_plural = "MP's"
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    party = models.CharField(max_length=30) 
    constituency = models.CharField(max_length=30)
    twitter_handle = models.CharField(max_length=30)

class Term(models.Model):
    class Meta:
        verbose_name = "Term"
        verbose_name_plural = "Terms"
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

class TermAlias(models.Model):
    class Meta:
        verbose_name = "Term Alias"
        verbose_name_plural = "Term Aliases"
    term = models.ForeignKey('Term')
    alias = models.CharField(max_length=30)

