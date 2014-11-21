__author__ = 'nlivni'
import django
from django.conf.urls import patterns, url
from models import Story
from panews.views import StoryDetailView, StoryListView, StoryTemplateCreate, StoryDelete, StoryUpdate, CategoryListView, StoryCustom, StorySuccessView
django.setup()

urlpatterns = patterns('',
    # url(r'^$', 'panews.views.home', name='home'),

    # homepage                          /
    url(r'^$',
        StoryListView.as_view(
            model=Story,
            template_name="home.html",
            context_object_name = "story_list"
                    )
        , name='home'),

    # create template                   /story/template/custom/
    url(r'^story/template/create/$', StoryTemplateCreate.as_view(), name='template_create'),

    # list of stories by category       /story/<category_slug>/
    url(r'^story/category/(?P<category_slug>[-_\w]+)/$', CategoryListView.as_view(), name='category_list'),



    # view completed story              /story/<story_id>/
    url(r'^story/(?P<slug>[-_\w]+)/$', StoryDetailView.as_view(),
        name='story_detail'
    ),

    # generic list of all stories       /story/
    url(r'^story/$',
        StoryListView.as_view(
            model=Story
                    )
        , name='story_list'),


    # custom story from story        /story/<story_slug>/custom/
    url(r'^story/(?P<slug>[-_\w]+)/custom', StoryCustom.as_view(), name='story_custom'),




    # URLS THAT REQUIRE LOGGING IN (CRUD OF AUTHOR'S OWN CONTENT)

    # update story          @login      /story/<story_id>/update/

    # update story template @login      /story/<story_id>/template/update/
    url(r'^story/(?P<edit_slug>[-_\w]+)/update$', StoryUpdate.as_view(), name='story_update'),
    url(r'^story/(?P<edit_slug>[-_\w]+)/success', StorySuccessView.as_view(), name='story_success'),

    # delete story template @login      /story/<story_id>/template/delete/
    url(r'^story/(?P<slug>[-_\w]+)/delete/$', StoryDelete.as_view(), name='story_delete'),

)