from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from panews.models import Story, Category


def home(request):
    return HttpResponse("<h1>hello world</h1>")


def get_category_list():
    category_list = []
    return category_list


class StoryDetailView(DetailView):
    context_object_name = "story"
    model = Story

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = Category.objects.all()
        return context


class StoryListView(ListView):
    context_object_name = "story"
    model = Story

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(StoryListView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = Category.objects.all()
        return context



