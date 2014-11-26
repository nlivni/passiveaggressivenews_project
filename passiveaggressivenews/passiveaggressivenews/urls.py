from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'', include('panews.urls')),
                       # url(r'^ckeditor/', include('ckeditor.urls')),
                        url(r'^photologue/', include('photologue.urls', namespace='photologue')),
                       url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)
