__author__ = 'nlivni'

from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from models import StoryGnome
from panews.views import GnomeStoryDetailView, GnomeStoryListView

urlpatterns = patterns('',
    url(r'^$', 'panews.views.home', name='home'),

    url(r'^story/(?P<slug>[-_\w]+)', GnomeStoryDetailView.as_view(),
        name='storygnome_detail'
    ),
    url(r'^story/',
        GnomeStoryListView.as_view(
            model=StoryGnome
                    )
        , name='storygnome_list'),

)