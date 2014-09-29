from django.contrib import admin

from panews.models import Category, StoryGnome, AssociatedSnippet
# Register your models here.

admin.site.register(Category)
admin.site.register(StoryGnome)
admin.site.register(AssociatedSnippet)