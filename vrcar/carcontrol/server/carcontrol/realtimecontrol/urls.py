from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'about/^$',  views.about, name='about'),
    url(r'^control/(?P<label>[\w-]{,50})/$', views.control, name='control'),
    url(r'^$',  views.dircontrol, name='dircontrol'),
    ]
