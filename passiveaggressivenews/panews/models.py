from django.db import models
from taggit.managers import TaggableManager
import uuid
import datetime
import ast
from django.core.urlresolvers import reverse_lazy
from django_bleach.models import BleachField


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


def make_uuid():
    return str(uuid.uuid4().int >> 64)


def get_current_date():
    return datetime.datetime.today()


def get_current_time():
    return datetime.datetime.now().time()

# @todo deprecated code based on nested arrays in listfield. remove once project is running.
# def create_variable_list(variable_list_array):
#         v_list = []
#         for v in variable_list_array:
#             v_list.append(v[0])
#         return v_list


def create_display_text(story):
    var_count = story.template.count("%s")

    while var_count > len(story.variables):
        story.variables.append('')

    new_variables = story.variables[:var_count]

    return story.template % tuple(new_variables)


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
    edit_slug = models.SlugField(max_length=255, unique=True, default=make_uuid)
    category = models.ForeignKey(Category, blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author_name = models.CharField(max_length=30, blank=True, null=True)
    author_email = models.EmailField(blank=True, null=True)
    template = BleachField(blank=True, null=True)
    variables = ListField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(editable=False)
    #auto get mod date
    modified = models.DateTimeField(default=datetime.datetime.now())
    from_template = models.ForeignKey('self', blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('story_detail', kwargs={'slug': self.slug})

    # The combination of the template and variables that is output to the page
    def display_text(self):
        return create_display_text(self)

    # def variable_list(self):
    #     return create_variable_list(self.variables)

    # On save, update timestamps
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(Story, self).save(*args, **kwargs)

    def __str__(self):
        return self.title