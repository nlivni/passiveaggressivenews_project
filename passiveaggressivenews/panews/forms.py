__author__ = 'nlivni'

from django.forms import ModelForm
from panews.models import Story


# todo: story creation form (from scratch w/variables)
# todo: story mod form (with variables) - no login required
"""
The form will need to be able to do the following:

    - modelform - be bound to an object

    - on GET:
        hide the variable field
        display the form

    - on POST:
        - convert json in hidden field to a list
        - clean data
        - test for an error on displaying the story
        - save
"""


class StoryForm(ModelForm):
    class Meta:
        model = Story


