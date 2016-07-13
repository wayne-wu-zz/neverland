from django.conf.urls import include, url
from .views import NeverlandView

urlpatterns = [
    url(r'^neverland/?$', NeverlandView.as_view)
]

