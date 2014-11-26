from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from panews.models import Story, Category
from django.core.urlresolvers import reverse_lazy
from forms import StoryTemplateForm, StoryCustomForm
from datetime import datetime
from passiveaggressivenews.settings import SITE_ID
from django.contrib.sites.models import Site
from django.db.models import Count

SITE_URL = Site.objects.get(pk=SITE_ID).domain

# @todo get general context that is sent to all views


def get_category_list():
    category_list = Category.objects.all()
    return category_list


def get_template_list():
    template_list = Story.objects.filter(from_template__isnull=True).annotate(child_count=Count('story')).order_by('child_count').reverse()
    return template_list


class StoryMixin(object):
    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(StoryMixin, self).get_context_data(**kwargs)
        context['SITE_URL'] = SITE_URL
        context['category_list'] = get_category_list()
        context['template_list'] = get_template_list()
        return context


class StoryFormMixin(object):

    def form_valid(self, form):
        form.send_email()
        return super(StoryFormMixin, self).form_valid(form)


class StoryDetailView(StoryMixin, DetailView):
    context_object_name = "story"
    model = Story


class CategoryListView(StoryMixin, ListView):
    context_object_name = "story_list"
    model = Story
    template_name = "panews/category_list.html"

    def get_queryset(self):
        slug = self.kwargs['category_slug']
        queryset = Story.objects.filter(category__slug=slug)
        return queryset


class StoryListView(StoryMixin, ListView):
    context_object_name = "story_list"
    model = Story

    def get_queryset(self):
        queryset = get_template_list()
        return queryset


class StoryCustom(StoryMixin, CreateView):
    model = Story
    form_class = StoryCustomForm
    template_name = "panews/story_custom_form.html"

    def get_success_url(self):
        edit_slug = self.object.edit_slug
        return reverse_lazy('story_success', kwargs={'edit_slug': edit_slug})

    def get_initial(self):
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
        initial['template'] = parent.template
        initial['variables'] = parent.variables
        initial['tags'] = parent.tags
        initial['modified'] = datetime.now()
        initial['from_template'] = parent.pk
        return initial

    def get_context_data(self, **kwargs):
        context = super(StoryCustom, self).get_context_data(**kwargs)
        parent_slug = self.kwargs.get('slug')
        parent = Story.objects.get(slug=parent_slug)
        context['object'] = parent
        return context


class StoryTemplateCreate(StoryMixin, StoryFormMixin, CreateView):
    model = Story
    form_class = StoryTemplateForm
    success_url = reverse_lazy('story_list')

    def get_success_url(self):
        edit_slug = self.object.edit_slug
        return reverse_lazy('story_success', kwargs={'edit_slug': edit_slug})


class StoryUpdate(StoryMixin, StoryFormMixin, UpdateView):
    model = Story
    template_name = 'panews/story_form.html'
    form_class = StoryTemplateForm
    slug_field = 'edit_slug'
    slug_url_kwarg = 'edit_slug'

    def get_success_url(self):
        edit_slug = self.kwargs['edit_slug']
        return reverse_lazy('story_success', kwargs={'edit_slug': edit_slug})


class StorySuccessView(StoryMixin, DetailView):
    context_object_name = "story"
    model = Story
    slug_field = 'edit_slug'
    slug_url_kwarg = 'edit_slug'
    template_name = 'panews/story_detail_success.html'

    def get_context_data(self, **kwargs):
        context = super(StorySuccessView, self).get_context_data(**kwargs)
        context['is_success_page'] = True
        return context


class StoryDelete(DeleteView):
    model = Story
    success_url = reverse_lazy('story_list')