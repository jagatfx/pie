from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('website.views',
    url(r'^$', 'home'),
    url(r'^dashboard/$', direct_to_template, {'template': 'dashboard.html', 'extra_context': {'dash':True}}),
    url(r'^about/$', direct_to_template, {'template': 'about.html', 'extra_context': {'about':True}}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('website.views',
    url(r'^politicos/$', 'politicos_overview', {'type': 'Politico'}),
    url(r'^politicos/LD/$', 'politicos_overview', {'type': 'LD'}),
    url(r'^politicos/LD/(?P<pol_name>[a-zA-Z_\'-]+)/$', 'politico_detail'),
    url(r'^politicos/MP/$', 'politicos_overview', {'type': 'MP'}),
    url(r'^politicos/MP/(?P<pol_name>[a-zA-Z_\'-]+)/$', 'politico_detail'),
    url(r'^media/$', 'media_overview'),
    url(r'^media/(?P<media_name>\w+)/$', 'media_detail'),
    #url(r'^issues/$', 'issues_overview'),
    #url(r'^issues/(?P<mp_name>\w+)/$', 'issues_detail'),
)

urlpatterns += patterns('website.views',
    url(r'^ajax/feed/$', 'live_tweet_feed'),
    url(r'^viz/$', 'visualizations'),
    url(r'^viz/(?P<viznum>[0-9]+)/$', 'see_visualization'),
)
