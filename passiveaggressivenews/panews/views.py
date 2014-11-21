from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from panews.models import Story, Category
from django.core.urlresolvers import reverse_lazy, reverse
from forms import StoryTemplateForm, StoryCustomForm
from datetime import datetime
from passiveaggressivenews.settings import SITE_ID
from django.contrib.sites.models import Site

# @todo get general context that is sent to all views


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
        # call the base implementation first to get a context
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        # add in a queryset of all the categories
        context['category_list'] = get_category_list()
        context['SITE_URL'] = Site.objects.get(pk=SITE_ID).domain
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
        # call the base implementation first to get a context
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category_list'] = get_category_list()
        context['category'] = Category.objects.get(slug=slug)
        context['SITE_URL'] = Site.objects.get(pk=SITE_ID).domain
        return context


class StoryListView(ListView):
    context_object_name = "story_list"
    model = Story

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(StoryListView, self).get_context_data(**kwargs)
        context['category_list'] = get_category_list()
        context['SITE_URL'] = Site.objects.get(pk=SITE_ID).domain
        return context

    def get_queryset(self):
        queryset = get_template_list()
        return queryset


class StoryTemplateCreate(CreateView):
    model = Story
    form_class = StoryTemplateForm
    success_url = reverse_lazy('story_list')

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(StoryTemplateCreate, self).get_context_data(**kwargs)
        context['category_list'] = get_category_list()
        return context

    def get_success_url(self):
        edit_slug = self.object.edit_slug
        return reverse_lazy('story_success', kwargs={'edit_slug': edit_slug})



class StoryCustom(CreateView):
    model = Story
    form_class = StoryCustomForm
    template_name = "panews/story_custom_form.html"

    def get_success_url(self):
        slug = self.kwargs['slug']
        edit_slug = Story.objects.get(slug=slug).edit_slug
        return reverse('story_success', kwargs={'edit_slug': edit_slug})




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
        # call the base implementation first to get a context
        context = super(StoryCustom, self).get_context_data(**kwargs)
        # add in a queryset of all the categories
        parent_slug = self.kwargs.get('slug')
        parent = Story.objects.get(slug=parent_slug)
        context['object'] = parent
        context['category_list'] = get_category_list()
        context['SITE_URL'] = Site.objects.get(pk=SITE_ID).domain

        return context


class StoryUpdate(UpdateView):
    model = Story
    template_name = 'panews/story_form.html'
    form_class = StoryTemplateForm
    slug_field = 'edit_slug'
    slug_url_kwarg = 'edit_slug'

    def get_success_url(self):
        edit_slug = self.kwargs['edit_slug']
        return reverse_lazy('story_success', kwargs={'edit_slug': edit_slug})

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(StoryUpdate, self).get_context_data(**kwargs)
        # add in a queryset of all the categories
        context['SITE_URL'] = Site.objects.get(pk=SITE_ID).domain
        context['category_list'] = get_category_list()
        return context


class StorySuccessView(DetailView):
    context_object_name = "story"
    model = Story
    slug_field = 'edit_slug'
    slug_url_kwarg = 'edit_slug'
    template_name = 'panews/story_detail_success.html'

    def get_context_data(self, **kwargs):
        # call the base implementation first to get a context
        context = super(StorySuccessView, self).get_context_data(**kwargs)
        # add in a queryset of all the categories
        context['SITE_URL'] = Site.objects.get(pk=SITE_ID).domain
        context['category_list'] = get_category_list()
        context['is_success_page'] = True
        return context


class StoryDelete(DeleteView):
    model = Story
    success_url = reverse_lazy('story_list')