from django.db import models
from taggit.managers import TaggableManager
import uuid

class Category(models.Model):
    """
    For the navigation bar. Each story has one and only one category.
    """
    name = models.CharField(max_length=30)


class StoryArchtype(models.Model):
    """
    This is an abstract base class for our hardcoded story models. If we get around to having
    """
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    tags = TaggableManager()
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class StoryGnome(models.Model):
    """
    This is the actual story. The template will contain the text of the story, this model contains the variables
    that will form the "story spine", also the fields of the form.
    """
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    summary = models.TextField()


class AssociatedSnippet(models.Model):
    """
    Appears at the side of the page. not clickable but relate to the general category
    """
    name = models.CharField(max_length=50)
    text = models.TextField()
# todo: create more generic story model

