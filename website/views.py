# Imports
from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import MP
from website.twitter import *


def home(request):
    return render_to_response('index.html', RequestContext(request, {"home": True}))

def mp_overview(request):
    mp_list = MP.objects.all()
    data = {"mp": True, "mps": []}
    for mp in mp_list:
        mp_desc = {"name":mp.name, "url":mp.name.replace(" ", "_")}
        data["mps"].append(mp_desc)

    return render_to_response('mp_overview.html', RequestContext(request, data))

def mp_detail(request, mp_name):
    mp = MP.objects.get(name=mp_name.replace('_', ' '))
    data = {"mp": True,
            "name": mp.name,
            "image_url": "http://pie.shreyaschand.com/img/mp/" + mp_name + ".png",
            "party": mp.party,
            "constituency": mp.constituency,
            "twitter_handle": mp.twitter_handle,
            "tweets_by_them": parse_tweet(latest_tweets(mp.twitter_handle)),
            "tweets_at_them": parse_tweet(relevant_tweets('', mp_twitter=mp.twitter_handle, only_at=True))}
    return render_to_response('mp_detail.html', RequestContext(request, data))

