__author__ = 'nlivni'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'panews.views.home', name='home'),
    url(r'^story/', 'panews.views.home', name='home'),
    url(r'^story/', 'panews.views.home', name='home'),

)
