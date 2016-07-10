from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',  views.dircarcontrol, name='dircarcontrol'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^about/$',  views.about, name='about'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
    url(r'^control/(?P<label>[\w-]{,50})/$', views.control, name='control'),
]
