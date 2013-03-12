# Imports
from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import MP
from website.twitter import *


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
        politico_list = MP.objects.all().order_by('name')
    else:
        politico_list = MP.objects.all().order_by('name')

    for politico in politico_list:
        politico_desc = {"name": politico.name,
                         "url": politico.name.replace(" ", "_"),
                         "party": politico.party,
                         "constituency": politico.constituency,
                         "type": "mp"} # to be looked up later from general data struct
        pols.append(politico_desc)

    return pols

def mp_detail(request, mp_name):
    mp = MP.objects.get(name=mp_name.replace('_', ' '))
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


def lord_detail(request, mp_name):
    mp = MP.objects.get(name=mp_name.replace('_', ' '))
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
