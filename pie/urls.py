from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pie.views.home', name='home'),
    # url(r'^pie/', include('pie.foo.urls')),
    url(r'^$', 'website.views.home'),
    url(r'^mp/$', 'website.views.mp_overview'),
    url(r'^mp/(?P<mp_name>\w+)/$', 'website.views.mp_detail'),
    url(r'^about/$', direct_to_template, {'template': 'about.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
