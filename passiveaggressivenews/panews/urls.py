__author__ = 'nlivni'

from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from models import StoryGnome

urlpatterns = patterns('',
    url(r'^$', 'panews.views.home', name='home'),

    url(r'^story/(?P<uuid>[-_\w]+)', DetailView.as_view(
        model=StoryGnome),
        name='storygnome_detail'
    ),
    url(r'^story/',
        ListView.as_view(
            model=StoryGnome
                    )
        , name='storygnome_list'),

)
