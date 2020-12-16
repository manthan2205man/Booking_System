import jwt, json

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from rest_framework import status, exceptions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from accounts.models import User, Token

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            msg = {"Status":HTTP_401_UNAUTHORIZED, "Message":"Invalid Method of token passing."}
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = {"Status":HTTP_401_UNAUTHORIZED, "Message":'Invalid token header. No credentials provided.'}
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = {"Status":HTTP_401_UNAUTHORIZED, "Message":'Invalid token header'}
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token=="null":
                msg = {"Status":HTTP_401_UNAUTHORIZED, "Message":'Null token not allowed'}
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = {"Status":HTTP_401_UNAUTHORIZED, "Message":'Invalid token header. Token string should not contain invalid characters.'}
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        email = payload['email']
        username = payload['username']
        
        try:
            user = User.objects.get(email=email, username=username)
            d_token = Token.objects.get(user=user)
            a_token = d_token.token

            if str(a_token) != str(token):
                msg = {"Status":HTTP_401_UNAUTHORIZED, "Message":"Token mismatch or Expired"}
                raise exceptions.AuthenticationFailed(msg)
               
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse(
                {"Status":HTTP_403_FORBIDDEN,'Message': "Token is invalid"},
                status="403"
            )
        except User.DoesNotExist:
            return HttpResponse(
                {"Status":HTTP_500_INTERNAL_SERVER_ERROR,'Message': "Internal server error"},
                status="500"
            )

        return (user, token)

    def authenticate_header(self, request):
        return 'Token'