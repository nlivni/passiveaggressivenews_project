from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from panews.models import Story, Category
from django.core.urlresolvers import reverse, reverse_lazy

from forms import StoryForm


def home(request):
    return HttpResponse("<h1>hello worldz</h1>")


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


class StoryCreate(CreateView):
    model = Story
    form_class = StoryForm
    success_url = reverse_lazy('story_list')


class StoryUpdate(UpdateView):
    # def get_success_url(self):
    #     if 'slug' in self.kwargs:
    #         slug = self.kwargs['slug']
    #     else:
    #         slug = 'demo'
    #     return reverse_lazy('/story/%s' % self.slug)
    model = Story
    form_class = StoryForm

class StoryDelete(DeleteView):
    model = Story
    success_url = reverse_lazy('story_list')