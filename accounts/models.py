from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
import datetime
# Create your models here.

today = datetime.date.today()

class User(AbstractUser):

    # is_owner = models.BooleanField(default=False)
    # is_customer = models.BooleanField(default=False)
    phone = models.BigIntegerField(null=True,validators=[RegexValidator(regex=r'\d{10}',message='Please Enter valid 10-digit Number.',code='invalid_number')])
    city = models.CharField(max_length=20,null=True)

    def __str__(self):
        return str(self.username)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    generated_on = models.DateTimeField(default=timezone.now)
    expire = models.DateTimeField()

    def __str__(self):
        return str(self.user)