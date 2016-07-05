from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'^control/$', views.control, name='control'),
    ]
