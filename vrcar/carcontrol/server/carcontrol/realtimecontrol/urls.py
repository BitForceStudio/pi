from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'^chatroom/(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
    ]
