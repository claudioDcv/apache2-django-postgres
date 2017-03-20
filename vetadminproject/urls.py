# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
    # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('medicalConsultation.urls')),
    url(r'^consulta/', include('medicalConsultation.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
