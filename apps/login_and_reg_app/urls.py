from django.conf.urls import url
from . import views
from ..wally_trips import views as wally_trips
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    # url(r'^success$', views.success),
    url(r'^success$', wally_trips.wally_index),
    url(r'^validate_login$', views.validate_login),
    url(r'^logout$', views.logout),
]
