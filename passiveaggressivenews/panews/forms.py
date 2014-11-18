__author__ = 'nlivni'

from django.forms import ModelForm
from panews.models import Story
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Reset, Submit, Button, Field
from crispy_forms.bootstrap import FormActions
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


class StoryTemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StoryTemplateForm, self).__init__(*args, **kwargs)
        # self.fields['template'].widget = CKEditorWidget

        self.helper = FormHelper()
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
                'template'
            ),
            Field(
                'variables',
                wrapper_class='hidden',
                # type="hidden",
            ),
                # Field(
                #     'from_template',
                #     wrapper_class='hidden',
                #     # type="hidden",
                # ),
            # Field(
            #     'author',
            #     wrapper_class='hidden',
            #     # type="hidden",
            # ),
            Field(
                'modified',
                wrapper_class='hidden',
                #type="hidden",

            ),
            FormActions(
                Submit('submit', 'Save changes'),
                Reset('reset', 'Reset'),
                Button('cancel', 'Cancel')
            ),
        )

    def clean(self):
        cleaned_data = super(StoryTemplateForm, self).clean()
        template = cleaned_data.get("template")
        variables = cleaned_data.get("variables")

        # if template and variables:
            #only do this if both variables are valid so far

            # raise forms.ValidationError("TypeError: There are too many or too few variables for the template."
            #                             "Please check to make sure that each variable matches a single %s "
            #                             "in the template." + "variables: " + str(len(v_list)) + variables)

    class Meta:
        model = Story
        fields = ['title', 'slug', 'template', 'variables', 'modified']


class StoryCustomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StoryCustomForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.error_text_inline = True
        self.helper.layout = Layout(
            Field(
                'title',
                type="hidden",
            ),
            Field(
                'slug',
                type="hidden",

            ),
            Field(
                'template',
                type="hidden",

            ),
            Field(
                'variables',
                wrapper_class='hidden',
                type="hidden",
            ),
            Field(
                'modified',
                type="hidden",

            ),
            FormActions(
                Submit('submit', 'Save changes'),
                Reset('reset', 'Reset'),
                Button('cancel', 'Cancel')
            ),
        )

    def clean(self):
        cleaned_data = super(StoryCustomForm, self).clean()
        template = cleaned_data.get("template")
        variables = cleaned_data.get("variables")

        # if template and variables:
            #only do this if both variables are valid so far

            # raise forms.ValidationError("TypeError: There are too many or too few variables for the template."
            #                             "Please check to make sure that each variable matches a single %s "
            #                             "in the template." + "variables: " + str(len(v_list)) + variables)

    class Meta:
        model = Story
        fields = ['title', 'slug', 'template', 'variables', 'modified']
