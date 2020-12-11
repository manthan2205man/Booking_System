from django.db import models
from django.contrib.auth import get_user_model
import datetime
# Create your models here.
today = datetime.date.today()


class Tool(models.Model):
    categories = (
        ('room', 'room'),
        ('bike', 'bike'),
        ('car', 'car'),
    )
    cities = (
        ('surat', 'surat'),
        ('bharuch', 'bharuch'),
        ('navsari', 'navsari'),
        ('valsad', 'valsad'),
    )
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100,null=True)
    category = models.CharField(max_length=20,null=True, choices=categories)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    created_date = models.DateTimeField(null=True,auto_now_add=True)
    to_date = models.DateField(null=True,auto_now_add=True)
    description = models.TextField(null=True)
    photo = models.ImageField(null=True,upload_to='owner/')
    price = models.IntegerField(null=True)
    address = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=20,null=True, choices=cities)
    rating = models.IntegerField(null=True)

    def __str__(self):
        return str(self.pk)+"-----"+str(self.owner)+"-----"+str(self.title)


class Booking(models.Model):
    status = (
        ('success', 'success'),
        ('pending', 'pending'),
    )

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='customer', null=True)
    tools = models.ForeignKey(Tool(), on_delete=models.CASCADE, related_name='tools' , null=True)
    created_date = models.DateTimeField(null=True,auto_now_add=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    pay_status = models.CharField(max_length=20,null=True, default='pending')
    amount = models.IntegerField(null=True)
    booked_days = models.IntegerField(null=True)
    booking_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.pk)+"-----"+str(self.tools)+"-----"+str(self.created_date)


class Location(models.Model):
    cities = (
        ('surat', 'surat'),
        ('bharuch', 'bharuch'),
        ('navsari', 'navsari'),
        ('valsad', 'valsad'),
    )
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    city = models.CharField(max_length=20,null=True, choices=cities)

    def __str__(self):
        return str(self.id)+"-----"+str(self.city)

class Payment(models.Model):
    status = (
        ('success', 'success'),
        ('pending', 'pending'),
    )
    order = models.ForeignKey(Booking(), on_delete=models.CASCADE, null=True)
    order_date = models.DateField(null=True, auto_now_add=True)
    status = models.CharField(max_length=20, null=True, default='pending', choices=status)
    amount = models.IntegerField(null=True)
    txn_id = models.CharField(max_length=50, null=True)
    bank_txn_id = models.IntegerField(null=True)
    txn_date = models.CharField(max_length=20, null=True)
    payment_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.id)+"-----"+str(self.order_id)

class MultiplePhotos(models.Model):
    tool = models.ForeignKey(Tool(), on_delete=models.CASCADE, null=True)
    photo1 = models.ImageField(null=True,upload_to='owner/multi/')
    photo2 = models.ImageField(null=True,upload_to='owner/multi/')
    photo3 = models.ImageField(null=True,upload_to='owner/multi/')
    photo4 = models.ImageField(null=True,upload_to='owner/multi/')

    def __str__(self):
        return str(self.tool)

class Save_Tools(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    tool = models.ForeignKey(Tool(), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)+"-----"+str(self.customer)

class Rating(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment(), on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(null=True)
    review = models.CharField(max_length=600,null=True)

    def __str__(self):
        return str(self.id)+"-----"+str(self.rating)