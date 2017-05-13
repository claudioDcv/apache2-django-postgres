# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib.auth.views import login

# urlpatterns = [
# ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', login, {
        'template_name': 'login.html'}, name="login"),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    #
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
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    print(settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^uploads/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
