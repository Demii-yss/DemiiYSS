from django.urls import path, include
from . import views
from .views import makegif
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tools.tests import *

urlpatterns = [
    path('', views.home, name='tools'),
    path('makegif/', makegif.as_view(), name='makegif')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
