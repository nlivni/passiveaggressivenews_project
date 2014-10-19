__author__ = 'nlivni'

from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from models import Story
from panews.views import StoryDetailView, StoryListView

urlpatterns = patterns('',
    url(r'^$', 'panews.views.home', name='home'),

    url(r'^story/(?P<slug>[-_\w]+)', StoryDetailView.as_view(),
        name='story_detail'
    ),
    url(r'^story/',
        StoryListView.as_view(
            model=Story
                    )
        , name='story_list'),

)