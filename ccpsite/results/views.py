__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.shortcuts import render
from rest_framework import routers, serializers, viewsets

from .models import SinglesResult, Source
from .serializers import SinglesResultSerializer, SourceSerializer


class SourceViewSet(viewsets.ModelViewSet):
    """Source result viewset"""

    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SinglesResultViewSet(viewsets.ModelViewSet):
    """Singles result viewset"""

    queryset = SinglesResult.objects.all()
    serializer_class = SinglesResultSerializer
