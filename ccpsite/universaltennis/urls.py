__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.urls import include, path
from rest_framework import routers, serializers, viewsets

from .views import PlayerViewSet, index

router = routers.DefaultRouter()
router.register(r"player", PlayerViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("index.html", index, name="index"),
]
