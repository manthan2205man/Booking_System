from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Tool)
admin.site.register(Location)
admin.site.register(Booking)