__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from rest_framework import exceptions, serializers

from .models import Player


class RoundingDecimalField(serializers.DecimalField):
    def to_internal_value(self, data):
        if data == "":
            return 0.0

        return super().to_internal_value(data)

    def validate_precision(self, value):
        return value


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """Player records serializer"""

    id = serializers.IntegerField()
    singles_utr = RoundingDecimalField(max_digits=16, decimal_places=14)
    doubles_utr = RoundingDecimalField(max_digits=16, decimal_places=14)
    my_utr_singles = RoundingDecimalField(max_digits=16, decimal_places=14)
    my_utr_doubles = RoundingDecimalField(max_digits=16, decimal_places=14)

    class Meta:
        model = Player
        fields = "__all__"
