from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$',views.index     ,name='index'),
    url(r'^readebay_goldriga/$',views.readebay_goldriga,name='readebay_goldriga'),
]
