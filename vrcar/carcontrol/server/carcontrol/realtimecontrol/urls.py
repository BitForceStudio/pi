from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'^control/(?P<label>[\w-]{,50})/$', views.control, name='control'),
    ]
