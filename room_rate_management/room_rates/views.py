from django.shortcuts import render,HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from django import forms

def home(request):
    return render(request , 'room_rates/homepage.html')

def calculate_price(request):
    try:
        context = {}
        if request.method == 'POST':
            room_id = request.POST.get('roomID')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            if startDate and endDate and startDate > endDate:
                raise forms.ValidationError('End date must be after the start date')
            if not startDate or not endDate:
                raise forms.ValidationError('Both dates are required')
                
            if room_id  :
                availableRooms = RoomRate.objects.filter(room_id = room_id)
            else :
                availableRooms = RoomRate.objects.all()
            
            final_prices = []
            messages = []
            for room in list(availableRooms):
                price , discount = room.calculate_total_price(startDate,endDate)
                final_prices.append(price)
                if discount:
                    messages.append({'text':f'Discount Applied {discount}','tag':"success"})
                else:
                    messages.append({'text':'No Discount Available','tag':'info'})
            context['zipped_data'] = zip(list(availableRooms) , final_prices , messages )
            return render(request , 'room_rates/results.html' , context)
            
    except Exception as e:
        return HttpResponse(f"Invalid Request: {e}")

class RoomRateViewSet(viewsets.ModelViewSet):
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer

class  OverriddenRoomRateViewSet(viewsets.ModelViewSet):
    queryset =  OverriddenRoomRate.objects.all()
    serializer_class =  OverriddenRoomRateSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class DiscountRoomRateViewSet(viewsets.ModelViewSet):
    queryset = DiscountRoomRate.objects.all()
    serializer_class = DiscountRoomRateSerializer

