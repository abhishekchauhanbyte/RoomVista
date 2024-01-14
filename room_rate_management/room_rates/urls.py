# room_rates/urls.py
from django.urls import path , include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'room-rates', RoomRateViewSet)
router.register(r'discount',DiscountViewSet)
router.register(r'overridden-room-rates',OverriddenRoomRateViewSet)
router.register(r'discount-room-rate',DiscountRoomRateViewSet)



urlpatterns = [
    path('', home , name="search-home"),
    path('results/', calculate_price , name="search-result"),
    path('api/v1/', include(router.urls ))
]
