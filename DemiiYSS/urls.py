from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tools.tests import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('tools/', include('tools.urls')),
    path('', include('homepage.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
