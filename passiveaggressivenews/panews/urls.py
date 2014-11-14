__author__ = 'nlivni'

from django.conf.urls import patterns, url
from models import Story
from panews.views import StoryDetailView, StoryListView, StoryCreate, StoryDelete, StoryUpdate

urlpatterns = patterns('',
    # url(r'^$', 'panews.views.home', name='home'),
    url(r'^$',
        StoryListView.as_view(
            model=Story,
            template_name="home.html"
                    )
        , name='home'),

    url(r'^story/add/$', StoryCreate.as_view(), name='story_create'),

    url(r'^story/(?P<slug>[-_\w]+)/$', StoryDetailView.as_view(),
        name='story_detail'
    ),
    url(r'^story/$',
        StoryListView.as_view(
            model=Story
                    )
        , name='story_list'),

    url(r'^story/(?P<slug>[-_\w]+)/update$', StoryUpdate.as_view(), name='story_update'),
    url(r'^story/(?P<slug>[-_\w]+)/delete/$', StoryDelete.as_view(), name='story_delete'),

)