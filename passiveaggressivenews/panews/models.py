from django.db import models
from taggit.managers import TaggableManager
import uuid
import datetime
import ast
from django.core.urlresolvers import reverse_lazy
from django_bleach.models import BleachField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill


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
    title = models.CharField(max_length=50, default="A man, a plan, a can of spam, a banana: Bananama!")
    slug = models.SlugField(max_length=255, unique=True, default=make_uuid)
    edit_slug = models.SlugField(max_length=255, unique=True, default=make_uuid)
    category = models.ForeignKey(Category, blank=True, null=True)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='story_images')
    display_image = ImageSpecField(source='image',
                                   processors=[ResizeToFit(400, 400)],
                                   format='JPEG',
                                   options={'quality': 60})
    icon_image = ImageSpecField(source='image',
                                   processors=[ResizeToFill(100, 100)],
                                   format='JPEG',
                                   options={'quality': 60})
    image_caption = models.CharField(blank=True, null=True, max_length=150)
    author_email = models.EmailField(blank=True, null=True)
    template = BleachField(blank=True, null=True, default="<p>Change this text in the template box below to create a "
                                                          "reusable story template with changeable variables. "
                                                          "You can use <strong><em>%s</em></strong> in the template "
                                                          "box to signify a variable that others will be able to "
                                                          "fill in later."
                                                          "<p>Happy journalism!</p>")
    variables = ListField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(editable=False)
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