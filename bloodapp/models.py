from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Bloodsell(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    type = models.CharField(
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        verbose_name='Required Blood Type'
    )
    # type=models.CharField(max_length=4)
    quantity=models.CharField(max_length=200)
    price=models.IntegerField()

class Blooddonate(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=70)
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    type = models.CharField(
        max_length=3,
        choices=BLOOD_TYPE_CHOICES,
        verbose_name='Donate Blood Type'
    )
    # type=models.CharField(max_length=4)
    mobile=models.CharField(max_length=10)
    address=models.TextField(max_length=100)

class Confirmbuydetails(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    type=models.CharField(max_length=4)
    quantity=models.CharField(max_length=2)
    price=models.ForeignKey(Bloodsell,on_delete=models.CASCADE,db_column='price')
    total_price=models.IntegerField(null=True,blank=True)
    mobile=models.CharField(max_length=10)
    email=models.CharField(max_length=70)

class Bloodorder(models.Model):
    orderid=models.CharField(max_length=150)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    type=models.CharField(max_length=4)
    quantity=models.CharField(max_length=2)
    mobile=models.CharField(max_length=10)
    email=models.CharField(max_length=70)

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Slider Image {self.id}"
