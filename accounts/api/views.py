import jwt

from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta

from accounts.models import User, Token
from accounts.api.authentication import TokenAuthentication
from accounts.api.serializers import UserCreationSerializer


from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


class UserCreatView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "Status":HTTP_200_OK,
                    "Message":"User Created Successfully",
                    "Result":serializer.data}, 
                status=HTTP_200_OK
            )
        return Response(
            data={
                "Status":HTTP_400_BAD_REQUEST,
                "Result":serializer.errors}, 
            status=HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args,**kwargs):
        if not request.data['email'] or not request.data['password']:
            return Response(
                data={
                    "Status":HTTP_400_BAD_REQUEST,
                    "Message":"Email and Password is must to login."},
                status=HTTP_400_BAD_REQUEST
            )
        email = request.data['email']
        password = request.data['password']

        user = authenticate(username=email, password=password)
        if user is None:
            return Response(
                data={
                    "Status":HTTP_400_BAD_REQUEST,
                    "Message":"Email or Password is Incorrect."},
                status=HTTP_400_BAD_REQUEST
            )

        payload = {
            "username":user.username,
            "email":user.email,
            "datetime": str(datetime.now())
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        try:
            d_token = Token.objects.get(user=user)
            d_token.token = jwt_token
            expire_time = datetime.today() + timedelta(hours=24)
            d_token.expire = expire_time
            d_token.save()
        except:
            expire_time = datetime.today() + timedelta(hours=24)
            d_token = Token.objects.create(user=user, token=jwt_token, expire=expire_time)

        return Response(
            data={
                "Status":HTTP_200_OK,
                "Message":"Login Successfully.",
                "Result":{"Token":jwt_token}
            }, 
            status=HTTP_200_OK
        )

class test(APIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = []

    def get(self, request, *args,**kwargs):
        print("USER: ", request.user)
        return Response("Success", status=HTTP_200_OK)