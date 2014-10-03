from django.db import models
from taggit.managers import TaggableManager
import uuid
import datetime


def make_uuid():
    return str(uuid.uuid1().int >> 64)


def get_current_date():
    return datetime.datetime.today()


def get_current_time():
    return datetime.datetime.now().time()


class Category(models.Model):
    """
    For the navigation bar. Each story has one and only one category.
    """
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name


class StoryArchtype(models.Model):
    """
    This is an abstract base class for our hardcoded story models. If we get around to having
    """
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    tags = TaggableManager(blank=True)
    #can't use out of the box w/class based models, which is the whole reason we're doing this.
    #uuid = models.CharField(default=uuid.uuid4, editable=False, max_length=128)
    slug = models.SlugField(max_length=255, unique=True, default=make_uuid)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class StoryGnome(StoryArchtype):
    """
    This is the actual story. The template will contain the text of the story, this model contains the variables
    that will form the "story spine", also the fields of the form.
    """
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    summary = models.TextField()
    city = models.CharField(max_length=90, default="Tokyo")
    street = models.CharField(max_length=90, default="Main Street")
    household = models.CharField(max_length=90, default="THE ")
    date = models.DateField(default=get_current_date())
    time = models.TimeField(default=get_current_time())
    subject_first_name = models.CharField(max_length=90, default="Bob")
    subject_last_name = models.CharField(max_length=90, default="Garfield")
    cleaned_object = models.CharField(max_length=90, default="dirty pizza plate")
    cleaned_location = models.CharField(max_length=90, default="on the table")
    catchphrase = models.CharField(max_length=90, default="I have a lot of work to do")
    excuse_this_time = models.CharField(max_length=90, default="I'm so tired from playing hockey.")
    what_subject_did_instead = models.CharField(max_length=90, default="I'm so tired from playing hockey.")



    def __str__(self):
        return self.title


class AssociatedSnippet(models.Model):
    """
    Appears at the side of the page. not clickable but relate to the general category
    """
    name = models.CharField(max_length=50)
    text = models.TextField()



# todo: create more generic story model