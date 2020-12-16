import re
from datetime import timedelta, datetime

from accounts.models import User, Token
from tools.models import Tool, Location, Booking, Rating, Save_Tools, Payment

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, ValidationError


class ToolCreationSerializer(ModelSerializer):
    class Meta:
        model = Tool
        fields = [
            'owner', 'title', 'category', 'latitude', 'longitude', 'to_date', 'description', 'photo', 'price', 'address', 'city',
        ]
        

class BookingCreationSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'customer', 'tools', 'from_date', 'to_date', 'booked_days', 'amount', 'booking_id',
        ]

class ToolUpdateSerializer(ModelSerializer):
    owner = serializers.CharField(read_only=True)
    class Meta:
        model = Tool
        fields = [
            'owner', 'title', 'category', 'latitude', 'longitude', 'description', 'photo', 'price', 'address', 'city',
        ]

class BookingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'customer', 'tools', 'from_date', 'to_date', 'pay_status', 'booked_days', 'amount', 
        ]