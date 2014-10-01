from django.db import models
from taggit.managers import TaggableManager
import uuid

def make_uuid():
    return str(uuid.uuid1().int>>64)

class Category(models.Model):
    """
    For the navigation bar. Each story has one and only one category.
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class StoryArchtype(models.Model):
    """
    This is an abstract base class for our hardcoded story models. If we get around to having
    """
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    tags = TaggableManager()
    #can't use out of the box w/class based models, which is the whole reason we're doing this.
    #uuid = models.CharField(default=uuid.uuid4, editable=False, max_length=128)
    id = models.CharField(max_length=36, primary_key=True, default=make_uuid)
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


    def __str__(self):
        return self.title


class AssociatedSnippet(models.Model):
    """
    Appears at the side of the page. not clickable but relate to the general category
    """
    name = models.CharField(max_length=50)
    text = models.TextField()



# todo: create more generic story model