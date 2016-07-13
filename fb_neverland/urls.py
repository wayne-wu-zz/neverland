from django.conf.urls import include, url
from .views import NeverlandView

urlpatterns = [
    url(r'^fb_neverland/?$', NeverlandView.as_view())
]

