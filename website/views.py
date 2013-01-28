from django.template import RequestContext
from django.shortcuts import render_to_response
from website.models import MP

def home(request):
    return render_to_response('base.html', RequestContext(request))

def mp_detail(request, mp_name):
    mp = MP.objects.get(name=mp_name.replace('_', ' '))
    data = {"name": mp.name,
            "party": mp.party,
            "constituency": mp.constituency,
            "twitter": mp.twitter_handle}
    return render_to_response('mp.html', RequestContext(request, data))
