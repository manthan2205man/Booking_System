import jwt, json, random, string

from datetime import datetime, timedelta, date

from accounts.api.authentication import TokenAuthentication
from accounts.api.permissions import  BookingOwnerOnly, ToolOwnerOnly

from tools.models import Tool, Booking, Location, Payment, Save_Tools, Rating
from tools.api.serializers import ToolCreationSerializer, BookingCreationSerializer, BookingUpdateSerializer, ToolUpdateSerializer

from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.serializers import ValidationError


class ToolCreatView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    serializer_class = ToolCreationSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = ToolCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['owner'] = user
            serializer.validated_data['to_date'] = (date.today())
            print(serializer.validated_data['to_date'])
            serializer.save()
            return Response(data={"Tool Created Successfully":serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class BookingCreatView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    serializer_class = BookingCreationSerializer

    def post(self, request, *args, **kwargs):
        data, user = request.data, request.user
        to_date, from_date = datetime.strptime(data['to_date'], "%Y-%m-%d").date(), datetime.strptime(data['from_date'], "%Y-%m-%d").date()
        try:
            tool = Tool.objects.get(id=data['tools'])
        except:
            raise ValidationError({"error":"Tool not Found."})
        if from_date <= tool.to_date:
            raise ValidationError({"error":f"Item is not available till {tool.to_date}"})
        if user == tool.owner:
            raise ValidationError({"error":"You Own this Tool, Owner can not Book own Tools."})
        days = ((to_date - from_date) + timedelta(days=1)).days
        amount = tool.price * days
        serializer = BookingCreationSerializer(data=data)
        booking_id = (user.first_name).upper() + str(''.join(random.choices(string.ascii_uppercase + string.digits, k=8)))
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['customer'] = user
            serializer.validated_data['amount'] = amount
            serializer.validated_data['booked_days'] = days
            serializer.validated_data['booking_id'] = booking_id
            serializer.save()
            return Response(data={"Booking Created Successfully":serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class BookingDeleteView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [BookingOwnerOnly]
    serializer_class = BookingUpdateSerializer

class ToolUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Tool.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [ToolOwnerOnly]
    serializer_class = ToolUpdateSerializer

class ToolListView(ListAPIView):
    queryset = Tool.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ToolUpdateSerializer

class ToolFilterView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = ToolUpdateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        category = data['category']
        location = data['location']
        from_date = datetime.strptime(data['from_date'], '%Y-%m-%d')
        # to_date = datetime.strptime(data['to_date'], '%Y-%m-%d')
        serializer = ToolUpdateSerializer(Tool.objects.filter(category=category, to_date__lte=from_date, city=location), many=True)
        return Response(serializer.data)

