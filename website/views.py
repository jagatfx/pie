# Imports
from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import Politico, Media
from website.twitter import *
from django.http import HttpResponse
import json


def home(request):
    return render_to_response('index.html', RequestContext(request, {"home": True}))

def politicos_overview(request, type):
    data = {"politico": True, "politicos": get_politico_overview(type), "title": "All " + type + "s"}
    return render_to_response('politico_overview.html', RequestContext(request, data))

def get_politico_overview(type):
    pols = []
    if type == "Lord":
        politico_list = []
    elif type == "MP":
        politico_list = Politico.objects.all().order_by('name')
    else:
        politico_list = Politico.objects.all().order_by('name')

    for politico in politico_list:
        politico_desc = {"name": politico.name,
                         "url": politico.name.replace(" ", "_"),
                         "party": politico.party,
                         "constituency": politico.constituency,
                         "type": "mp"} # to be looked up later from general data struct
        pols.append(politico_desc)

    return pols

def mp_detail(request, mp_name):
    mp = Politico.objects.get(name=mp_name.replace('_', ' '))
    data = {"politico": True,
            "name": mp.name,
            "image_url": "http://pie.shreyaschand.com/img/mp/" + mp_name + ".png",
            "party": mp.party,
            "constituency": mp.constituency,
            "twitter_handle": mp.twitter_handle,
            "tweets_by_them": tweets_by(mp.twitter_handle),
            "tweets_at_them": tweets_at(mp.twitter_handle),
            "pageviews": 0 # TODO abstract this and move somewhere else later...
            }
    return render_to_response('politico_detail.html', RequestContext(request, data))


def lord_detail(request, mp_name):
    mp = Politico.objects.get(name=mp_name.replace('_', ' '))
    data = {"politico": True,
            "name": mp.name,
            "image_url": "http://pie.shreyaschand.com/img/mp/" + mp_name + ".png",
            "party": mp.party,
            "constituency": mp.constituency,
            "twitter_handle": mp.twitter_handle,
            "tweets_by_them": tweets_by(mp.twitter_handle),
            "tweets_at_them": tweets_at(mp.twitter_handle)
            }
    return render_to_response('politico_detail.html', RequestContext(request, data))

def live_tweet_feed(request):
    return HttpResponse(json.dumps(tweets_all()), content_type="application/json")

def media_overview(request):
    meds = []
    media_list = Media.objects.all().order_by('name')

    for media in media_list:
        media_desc = {"name": media.name,
                      "url": media.name.replace(" ", "_"),
                      "party_leaning": media.party_leaning,
                      "affiliation": media.affiliation}
        meds.append(media_desc)
    data = {"media": True, "medias": meds, "title": "All Media Personalities"}
    return render_to_response('media_overview.html', RequestContext(request, data))

def media_detail(request, media_name):
    media = Media.objects.get(name=media_name.replace('_', ' '))
    data = {"politico": True,
            "name": media.name,
            "image_url": "http://pie.shreyaschand.com/img/media/" + media_name + ".png",
            "party_leaning": media.party_leaning,
            "affiliation": media.affiliation,
            "twitter_handle": media.twitter_handle,
            "tweets_by_them": tweets_by(media.twitter_handle),
            "tweets_at_them": tweets_at(media.twitter_handle)
            }
    return render_to_response('media_detail.html', RequestContext(request, data))

def visualizations(request):
    return render_to_response('viz.html', RequestContext(request))

def see_visualization(request, viznum):
    return render_to_response('viz{0}.html'.format(viznum), RequestContext(request))
