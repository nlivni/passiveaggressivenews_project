from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from panews.models import StoryGnome, Category

def home(request):
    return HttpResponse("<h1>hello world</h1>")


class GnomeStoryDetailView(DetailView):
    context_object_name = "story"
    model = StoryGnome

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(GnomeStoryDetailView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = Category.objects.all()
        return context


class GnomeStoryListView(ListView):
    context_object_name = "story"
    model = StoryGnome

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(GnomeStoryListView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = Category.objects.all()
        return context
