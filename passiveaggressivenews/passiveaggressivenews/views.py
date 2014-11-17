__author__ = 'nlivni'

from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>this is being served by the sotewide urls.py</h1>")
