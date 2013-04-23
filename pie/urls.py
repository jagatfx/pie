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
    url(r'^politicos/lord/$', 'politicos_overview', {'type': 'Lord'}),
    url(r'^politicos/lord/(?P<mp_name>[a-zA-Z_\'-]+)/$', 'lord_detail'),
    url(r'^politicos/mp/$', 'politicos_overview', {'type': 'MP'}),
    url(r'^politicos/mp/(?P<mp_name>[a-zA-Z_\'-]+)/$', 'mp_detail'),
    url(r'^media/$', 'media_overview'),
    url(r'^media/(?P<media_name>\w+)/$', 'media_detail'),
    #url(r'^issues/$', 'issues_overview'),
    #url(r'^issues/(?P<mp_name>\w+)/$', 'issues_detail'),
)

urlpatterns += patterns('website.views',
    url(r'^ajax/feed/$', 'live_tweet_feed'),
)
