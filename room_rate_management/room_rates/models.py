# room_rates/models.py
from django.db import models
from .constants import CONSTANTS
from datetime import datetime, timedelta
class RoomRate(models.Model):
    room_id = models.IntegerField()
    room_name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_price(self , startDate, endDate):
        totalPrice = 0
        current_date = startDate
        while current_date <= endDate:
            price , discount = self.calculate_final_rate(current_date)
            totalPrice +=  price

            # Define the date as a datetime object
            date_string = current_date
            date_format = "%Y-%m-%d"
            date = datetime.strptime(date_string, date_format)
            # Calculate the next day
            next_day = date + timedelta(days=1)
            
            # Convert the next day back to a string
            current_date = next_day.strftime(date_format)
        return totalPrice , discount


    #calculate the final lowest price including discount for a given date.
    def calculate_final_rate(self, date):
        try:
            overridden_rate_model = OverriddenRoomRate.objects.get(room_rate = self.pk , stay_date = date
)
        except OverriddenRoomRate.DoesNotExist:
            
            overridden_rate_model = None
        
        discounts_applicable_models = list(DiscountRoomRate.objects.filter(room_rate = self.pk))
        
        lowest_price_possible =  overridden_rate_model.overridden_rate if overridden_rate_model else self.default_rate
        if len(discounts_applicable_models):
            max_discount , discount_applied = RoomRate.get_maximum_discount(discounts_applicable_models,lowest_price_possible)
            return lowest_price_possible - max_discount , discount_applied 
        return round(lowest_price_possible , 2) , None
    
    @staticmethod
    def get_maximum_discount(discounts_applicable_models , price):
        max_discount = 0
        discount_applied = ""
        for d in discounts_applicable_models:
            curr_discount = 0
            if not isinstance(d, DiscountRoomRate):
                continue
            if d.discount.discount_type == CONSTANTS['DISCOUNT_TYPES_PERCENTAGE'] and d.discount.discount_value > 0.00 and d.discount.discount_value < 100.00:
                curr_discount = price*(d.discount.discount_value)/100    
            elif d.discount.discount_type == CONSTANTS['DISCOUNT_TYPES_FIXED']  and d.discount.discount_value > 0 and d.discount.discount_value < price:
                curr_discount = d.discount.discount_value
            if max_discount < curr_discount:
                max_discount = curr_discount
                discount_applied = str(d.discount.discount_name)
        return round(max_discount, 2) , discount_applied

    def __str__(self) -> str:
        return "Room :"+self.room_name

class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    overridden_rate = models.DecimalField(max_digits=10, decimal_places=2)
    stay_date = models.DateField()

    def __str__(self) -> str:
        return "Overriden rate for room :"+self.room_rate.room_name

class Discount(models.Model):
    discount_id = models.IntegerField()
    discount_name = models.CharField(max_length=100)
    DISCOUNT_TYPES = (
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage'),
    )
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return "Discount :"+self.discount_name

class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return " For Room :"+self.room_rate.room_name+" discount is :"+ self.discount.discount_name
