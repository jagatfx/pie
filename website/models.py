from django.db import models

# Create your models here.

class MP(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    party = models.CharField(max_length=30) 
    constituency = models.CharField(max_length=30)
    twitter_handle = models.CharField(max_length=30)

class Term(models.Model):
    title = models.CharField(max_length=30)

class TermAliase(models.Model):
    term = models.ForeignKey('Term')
    alias = models.CharField(max_length=30)

