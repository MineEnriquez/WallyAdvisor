from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.wally_index),
    url(r'^trips/create$', views.trip_create),
    url(r'^trips/new$', views.trip_create_render),
    url(r'^dashboard$', views.dashboard_render),
    url(r'^trips/(?P<trip_id>\d+)$', views.view_trip),
    url(r'^trips/edit/(?P<trip_id>\d+)$', views.trip_edit),
    url(r'^trips/update/(?P<trip_id>\d+)$', views.trip_update),
    url(r'^trips/remove/(?P<trip_id>\d+)$', views.trip_remove),
    url(r'^trips/weather/(?P<trip_id>\d+)$', views.trip_weather),
]