__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from rest_framework import exceptions, serializers

from .models import SinglesResult, Source


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    """Source records serializer"""

    class Meta:
        model = Source
        fields = "__all__"


class SinglesResultSerializer(serializers.HyperlinkedModelSerializer):
    """Singles result records serializer"""

    class Meta:
        model = SinglesResult
        fields = "__all__"
