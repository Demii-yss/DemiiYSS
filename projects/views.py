from django.urls import path
from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request, 'projects.html')


urlpatterns = [
    path('', home)
]
