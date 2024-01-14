from rest_framework import routers, serializers
from .models import *
class RoomRateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = RoomRate
        fields = '__all__'
        
class OverriddenRoomRateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = OverriddenRoomRate
        fields = '__all__'

class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Discount
        fields = '__all__'

class DiscountRoomRateSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = DiscountRoomRate
        fields = '__all__'