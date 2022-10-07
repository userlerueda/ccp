__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.urls import include, path
from rest_framework import routers, serializers, viewsets

from .views import SinglesResultViewSet, SourceViewSet

router = routers.DefaultRouter()
router.register(r"singlesresult", SinglesResultViewSet)
router.register(r"source", SourceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
