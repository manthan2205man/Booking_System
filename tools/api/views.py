import jwt, json, random, string
import requests
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.conf import settings
from tools.paytm import Checksum
from datetime import datetime, timedelta, date

from accounts.api.authentication import TokenAuthentication
from accounts.api.permissions import  BookingOwnerOnly, ToolOwnerOnly

from tools.models import Tool, Booking, Location, Payment, Save_Tools, Rating
from tools.api.serializers import ToolCreationSerializer, BookingCreationSerializer, BookingUpdateSerializer, ToolUpdateSerializer

from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
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
        for i in data:
            if data.get(i) == "":
                return Response(
                    data={"Status":HTTP_400_BAD_REQUEST, "Message":f"{str(i).title()} field may not be blank."}, 
                    status=HTTP_400_BAD_REQUEST
                )
        serializer = ToolCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['owner'] = user
            serializer.validated_data['to_date'] = (date.today())
            # print(serializer.validated_data['to_date'])
            serializer.save()
            return Response(
                data={
                    "Status":HTTP_200_OK,
                    "Message":"Tool Created Successfully",
                    "Result":serializer.data},
                status=HTTP_200_OK
            )
        return Response(
            data={
                "Status":HTTP_400_BAD_REQUEST,
                "Result":serializer.errors},
            status=HTTP_400_BAD_REQUEST
        )

class BookingCreatView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    serializer_class = BookingCreationSerializer

    def post(self, request, *args, **kwargs):
        data, user = request.data, request.user
        for i in data:
            if data.get(i) == "":
                return Response(
                    data={"Status":HTTP_400_BAD_REQUEST, "Message":f"{str(i).title()} field may not be blank."}, 
                    status=HTTP_400_BAD_REQUEST
                )
        to_date, from_date = datetime.strptime(data['to_date'], "%Y-%m-%d").date(), datetime.strptime(data['from_date'], "%Y-%m-%d").date()

        try:
            tool = Tool.objects.get(id=data['tools'])
        except:
            return Response(
                data={"Status":HTTP_400_BAD_REQUEST, "Message":"Tool with given Tool ID not Found."},
                status=HTTP_400_BAD_REQUEST
            )
        if from_date <= tool.to_date:
            return Response(
                data={"Status":HTTP_400_BAD_REQUEST, "Message":f"Item is not available till {tool.to_date}"},
                status=HTTP_400_BAD_REQUEST
            )
        if user == tool.owner:
            return Response(
                data={"Status":HTTP_400_BAD_REQUEST, "Message":"You Own this Tool, Owner can not Book own Tools."},
                status=HTTP_400_BAD_REQUEST
            )
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
            return Response(
                data={
                    "Status":HTTP_200_OK,
                    "Message":"Booking Created Successfully",
                    "Result":serializer.data},
                status=HTTP_200_OK
            )
        return Response(
            data={
                "Status":HTTP_400_BAD_REQUEST,
                "Result":serializer.errors},
            status=HTTP_400_BAD_REQUEST
        )

class BookingDeleteView(RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [BookingOwnerOnly]
    serializer_class = BookingUpdateSerializer

class ToolUpdateView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [ToolOwnerOnly]
    serializer_class = ToolUpdateSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):        
        try:
            tool = ToolUpdateSerializer(Tool.objects.get(owner=request.user, id=self.kwargs.get('pk')))
            return Response(
                data={"Status":HTTP_200_OK,
                "Result":tool.data},
                status=HTTP_200_OK
            )
        except:
            return Response(
                data={"Status":HTTP_400_BAD_REQUEST,
                "Message":"Tool Not Found or You do not Own this Tool."},
                status=HTTP_400_BAD_REQUEST
            )
    def put(self, request, *args, **kwargs):
        try:
            tool = Tool.objects.get(owner=request.user, id=self.kwargs.get('pk'))
            data = request.data
            for i in data:
                if data.get(i) == "":
                    return Response(
                        data={"Status":HTTP_400_BAD_REQUEST, "Message":f"{str(i).title()} field may not be blank."}, 
                        status=HTTP_400_BAD_REQUEST
                    )
            tool.title, tool.category, tool.latitude, tool.longitude, tool.description, tool.photo, tool.price, tool.address, tool.city = data['title'], data['category'], data['latitude'], data['longitude'], data['description'], data['photo'], data['price'], data['address'], data['city']
            tool.save()
            tool = ToolUpdateSerializer(tool)
            return Response(
                data={"Status":HTTP_200_OK,
                "Result":tool.data},
                status=HTTP_200_OK
            )
        except:
            return Response(
                data={"Status":HTTP_400_BAD_REQUEST,
                "Message":"Tool Not Found or You do not Own this Tool."},
                status=HTTP_400_BAD_REQUEST
            )


class ToolListView(APIView):
    # queryset = Tool.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ToolUpdateSerializer

    def get(self, request, *args, **kwargs):        
        try:
            tools = ToolUpdateSerializer(Tool.objects.all())
            print("AAAAAAA", tools.data)
            return Response(
                data={"Status":HTTP_200_OK,
                "Result":tools.data},
                status=HTTP_200_OK
            )
        except:
            return Response(
                data={"Status":HTTP_400_BAD_REQUEST,
                "Message":"No Tools Found."},
                status=HTTP_400_BAD_REQUEST
            )
class ToolFilterView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = ToolUpdateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        category = data['category']
        location = data['location']
        from_date = datetime.strptime(data['from_date'], '%Y-%m-%d')
        # to_date = datetime.strptime(data['to_date'], '%Y-%m-%d')
        serializer = ToolUpdateSerializer(Tool.objects.filter(category=category, city=location), many=True)
        return Response(serializer.data)

MERCHANT_KEY=str(settings.PAYTM_MERCHANT_KEY)

@api_view()
def order(request, pk):
    try:
        obj = Booking.objects.get(id=pk)
    except:
        messages.error(request, "Booking Not Found")
        return redirect('home')
    user_name = str(obj.tools.owner.first_name).upper()
    cus_name = str(request.user.first_name).upper()
    orderid = user_name[0] + cus_name + str(''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))

    Payment.objects.create(order=obj, amount=obj.amount, payment_id=orderid)

    param_dict = {
        'MID': str(settings.PAYTM_MERCHANT_ID),
        'ORDER_ID': str(orderid),
        'TXN_AMOUNT': str(obj.amount),
        'CUST_ID': '5',
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',  # for testing
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/tools/api/handlerequest/',
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return Response({'param_dict': param_dict})

#    ''' To render on our template, like web page on application. '''
    # return render(request, 'payment/paytm.html', {'param_dict': param_dict})

@api_view()
@csrf_exempt
def handlerequest(request):  # paytm will send POST request herre
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            obj = Payment.objects.get(payment_id=response_dict['ORDERID'])
            obj.status = 'success'
            obj.txn_id = response_dict['TXNID']
            obj.bank_txn_id = response_dict['BANKTXNID']
            obj.txn_date = response_dict['TXNDATE']
            obj.save()

            tool = Tool.objects.get(id=obj.order.tools.id)
            tool.to_date = obj.order.to_date+timedelta(days=1)
            tool.save()

            book = Booking.objects.get(id=obj.order.id)
            book.pay_status = 'success'
            book.save()

            message = f'Hello {book.customer.first_name}  \n\nYour booking is Confirm \n\n Your Booking Details are' \
                    f'Booking ID : {book.booking_id}\n' \
                    f'Booking From Date : {book.from_date} \n' \
                    f'Booking To Date : {book.to_date} \n' \
                    f'Booking Days : {book.booked_days} \n' \
                    f'Amount for payment : {book.amount} \n' \
                    f'Payment Status : {obj.status}\n' \
                    f'Transaction Id : {obj.txn_id} \n' \
                    f'Bank Transaction Id: {obj.bank_txn_id} \n' \
                    f'Bank Transaction Date : {obj.txn_date} \n' \
                    f'Paied Amount : {obj.amount} \n'
            send_mail('Booking Confirmation', message, settings.EMAIL_HOST_USER, [book.customer], fail_silently=True)

        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return Response({'response': response_dict})