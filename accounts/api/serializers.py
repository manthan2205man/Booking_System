import re

from accounts.models import User, Token

from rest_framework.serializers import ModelSerializer, CharField, ValidationError


class UserCreationSerializer(ModelSerializer):
    password2 = CharField(label='Confirm Password')
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'city',
        ]
        extra_kwargs = {'password':{'write_only':True}}

    def validate_email(self, value):
        email = value
        try:
            user = User.objects.get(username=email)
        except:
            user = None
        if user is not None:
            raise ValidationError("Email is already registered.")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password2 = value
        password = data.get('password')
        if password != password2:
            raise ValidationError("Password and Confirm Password didn't match.")
        return value

    def create(self, validated_data):
        email = str(validated_data['email']).lower()
        password = validated_data['password']
        first_name = str(validated_data['first_name']).title()
        last_name = str(validated_data['last_name']).title()
        phone = validated_data['phone']
        city = str(validated_data['city']).title()
        user_obj = User(username=email, email=email, first_name=first_name, last_name=last_name,  phone=phone, city=city)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data