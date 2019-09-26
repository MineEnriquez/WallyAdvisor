from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.wally_index),
    url(r'^dashboard$', views.dashboard_render),
    url(r'^request_weather$', views.read_weather),
    url(r'^trips/create$', views.trip_create),
    url(r'^trips/new$', views.trip_create_render),
]