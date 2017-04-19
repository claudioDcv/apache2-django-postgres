# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# urlpatterns = [
    # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('medicalConsultation.urls')),
    url(r'^consulta/', include('medicalConsultation.urls')),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
    #     'document_root': settings.STATIC_ROOT
    # }),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #     'document_root': settings.MEDIA_ROOT
    # }),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    print(settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^uploads/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
