from django.db import models
from taggit.managers import TaggableManager
import uuid
import datetime
import ast
import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class ListField(models.TextField):
    """
    ListField stores a python list in a model.
    http://brunorocha.org/python/django/django-listfield-e-separetedvaluesfield.html
    """
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def value_to_json(self, obj):
        value = self._get_val_from_obj(obj)
        return json.dumps(self.get_db_prep_value(value))


def make_uuid():
    return str(uuid.uuid1().int >> 64)


def get_current_date():
    return datetime.datetime.today()


def get_current_time():
    return datetime.datetime.now().time()


def create_display_text(story):
        return story.content % tuple(story.variable_list())


class Category(models.Model):
    """
    For the navigation bar. Each story has one and only one category.
    """
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name


class Story(models.Model):
    """
    generic story model
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, default=make_uuid)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    variables = ListField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('story-detail', kwargs={'slug': self.slug})


    # The combination of the content and variables that is output to the page
    def display_text(self):
        return create_display_text(self)

    def variable_list(self):
        v_list = []
        for v in self.variables:
            v_list.append(v[0])
        return v_list

    # On save, update timestamps
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(Story, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
