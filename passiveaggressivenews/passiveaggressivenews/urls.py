from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'passiveaggressivenews.views.home', name='home'),
    url(r'^$', include('panews.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
