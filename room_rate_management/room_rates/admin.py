from django.contrib import admin
from .models import Discount , RoomRate ,DiscountRoomRate ,OverriddenRoomRate
# Register your models here.
admin.site.register(Discount)
admin.site.register(RoomRate)
admin.site.register(DiscountRoomRate)
admin.site.register(OverriddenRoomRate)