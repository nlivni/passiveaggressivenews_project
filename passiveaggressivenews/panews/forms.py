__author__ = 'nlivni'

from django.forms import ModelForm
from panews.models import Story
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Reset, Submit, Button, Field
from crispy_forms.bootstrap import FormActions
from django.core.mail import EmailMessage
# from panews.views import SITE_URL
from django.core.urlresolvers import reverse_lazy
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


# @todo this is duplicated in views.py but caused an error on import of SITE_URL.
from passiveaggressivenews.settings import SITE_ID
from django.contrib.sites.models import Site
SITE_URL = Site.objects.get(pk=SITE_ID).domain


class StoryTemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StoryTemplateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'story_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Field(
                'title'
            ),
            Field(
                'slug',
                type="hidden",

            ),
            Field(
                'edit_slug',
                type="hidden",

            ),
            Field(
                'template'
            ),
            Field(
                'image'
            ),
            Field(
                'variables',
                wrapper_class='hidden',
                # type="hidden",
            ),
            # Field(
            #     'author_name',
            #
            # ),
            Field(
                'author_email',

            ),
            Field(
                'modified',
                wrapper_class='hidden',
                #type="hidden",

            ),
            Field(
                'from_template',
                type="hidden",

            ),
            FormActions(
                Submit('submit', 'Save changes'),
                Reset('reset', 'Reset'),
                Button('cancel', 'Cancel')
            ),
        )

    def send_email(self):
        if self.cleaned_data['author_email']:
            author_email = self.cleaned_data['author_email']
            title = self.cleaned_data['title']
            slug = self.cleaned_data['slug']
            edit_slug = self.cleaned_data['edit_slug']
            view_url = SITE_URL + unicode(reverse_lazy('story_detail', kwargs={'slug': slug}))
            edit_url = SITE_URL + unicode(reverse_lazy('story_update', kwargs={'edit_slug': edit_slug}))
            content = """
            Thanks for using Fill In The News \n
            You can view your story here: %s \n
            You can edit your story here: %s\n
            Keep the edit link safe because it will allow anyone to change the story.\n
            \n
            If you have any questions, concerns, or just some good news please send us an email at fillinthenews@twoifiplay.com.
            """
            email = EmailMessage(
                'Fill In The News: %s' % title,
                content % (view_url, edit_url),
                to=[author_email, 'fillinthenews@twoifiplay.com']
            )
            email.send()
        pass

    class Meta:
        model = Story
        fields = ['title', 'slug', 'edit_slug', 'template', 'image', 'variables', 'modified', 'author_email', 'from_template']


class StoryCustomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StoryCustomForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.error_text_inline = True
        self.helper.form_id = 'story_form'
        self.helper.layout = Layout(
            Field(
                'title',
                # type="hidden",
            ),
            Field(
                'image',
                # type="hidden",
            ),
            Field(
                'slug',
                type="hidden",

            ),
            Field(
                'edit_slug',
                type="hidden",

            ),
            Field(
                'template',
                # type="hidden",
                wrapper_class='hidden',

            ),
            Field(
                'variables',
                wrapper_class='hidden',
                type="hidden",
            ),
            Field(
                'author_email',
                type="hidden",
            ),
            # Field(
            #     'author_name',
            #     wrapper_class='hidden',
            #     type="hidden",
            # ),
            Field(
                'modified',
                type="hidden",

            ),
            Field(
                'from_template',
                type="hidden",

            ),
            # FormActions(
            #     Submit('submit', 'Save changes'),
            #     Reset('reset', 'Reset'),
            #     Button('cancel', 'Cancel')
            # ),
        )


    class Meta:
        model = Story
        fields = ['title', 'slug', 'edit_slug', 'template','image', 'from_template', 'variables', 'modified', 'author_email']
