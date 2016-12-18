from __future__ import unicode_literals

from django.db import models


class Hotel(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.IntegerField()
    description = models.TextField(null=True)

    class Meta:
        db_table = 'hotel'


class Client(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=13)

    class Meta:
        db_table = 'client'


class Room(models.Model):
    number_of_people = models.IntegerField()
    price = models.FloatField()
    is_lux = models.BooleanField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'room'


class CheckIn(models.Model):
    date = models.DateField()
    days = models.IntegerField()
    total_price = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = 'check_in'
