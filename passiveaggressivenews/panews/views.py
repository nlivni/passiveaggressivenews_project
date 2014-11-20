from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from panews.models import Story, Category
from django.core.urlresolvers import reverse_lazy
from forms import StoryTemplateForm, StoryCustomForm
from datetime import datetime
from django import forms
from django_bleach.forms import BleachField
# @todo this is outdated. remove
def home(request):
    return HttpResponse("<h1>this is being serverved by the panews 'home'</h1>")


def get_category_list():
    category_list = Category.objects.all()
    return category_list


def get_template_list():
    template_list = Story.objects.filter(from_template__isnull=True)
    return template_list


class StoryDetailView(DetailView):
    context_object_name = "story"
    model = Story

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = get_category_list()
        return context


class CategoryListView(ListView):
    context_object_name = "story_list"
    model = Story
    template_name = "panews/category_list.html"

    def get_queryset(self):
        slug = self.kwargs['category_slug']
        queryset = Story.objects.filter(category__slug=slug)
        return queryset

    def get_context_data(self, **kwargs):
        slug = self.kwargs['category_slug']
        #call the base implementation first to get a context
        context = super(CategoryListView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = get_category_list()
        context['category'] = Category.objects.get(slug=slug)
        return context


class StoryListView(ListView):
    context_object_name = "story_list"
    model = Story

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(StoryListView, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        context['category_list'] = get_category_list()
        return context

    def get_queryset(self):
        queryset = get_template_list()
        return queryset


class StoryTemplateCreate(CreateView):
    model = Story
    form_class = StoryTemplateForm
    success_url = reverse_lazy('story_list')


class StoryCustom(CreateView):
    model = Story
    form_class = StoryCustomForm
    success_url = reverse_lazy('story_list')
    template_name = "panews/story_custom_form.html"
    # template = forms.CharField(widget=CKEditorWidget())

    def get_initial(self):
        if self.request.user:
            user = self.request.user
        # Get the initial dictionary from the superclass method
        initial = super(StoryCustom, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        parent_slug = self.kwargs.get('slug')
        parent = Story.objects.get(slug=parent_slug)
        initial['title'] = parent.title
        initial['subtitle'] = parent.subtitle
        initial['category'] = parent.category
        initial['description'] = parent.description
        initial['author'] = user
        initial['template'] = parent.template
        initial['variables'] = parent.variables
        initial['tags'] = parent.tags
        initial['modified'] = datetime.now()
        initial['from_template'] = parent.pk
        return initial

    def get_context_data(self, **kwargs):
        #call the base implementation first to get a context
        context = super(StoryCustom, self).get_context_data(**kwargs)
        #add in a queryset of all the categories
        parent_slug = self.kwargs.get('slug')
        parent = Story.objects.get(slug=parent_slug)
        context['object'] = parent
        return context


class StoryUpdate(UpdateView):
    model = Story
    form_class = StoryTemplateForm
    # template = BleachField()


class StoryDelete(DeleteView):
    model = Story
    success_url = reverse_lazy('story_list')