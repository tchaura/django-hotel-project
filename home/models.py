import uuid

from django.db import models
import datetime
import django
from datetime import timezone
from django.utils import timezone

# Create your models here.


class Room(models.Model):
    capacity = models.IntegerField()
    COMFORTABILITY_CHOICES = [
        ("lux", "Люкс"),
        ("semi-lux", "Полу-люкс"),
        ("standard", "Обычный"),
    ]
    comfortability = models.CharField(choices=COMFORTABILITY_CHOICES, max_length=20)
    number = models.IntegerField()
    floor = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"Room number {self.number}"


class Order(models.Model):
    timezone.activate('Europe/Minsk')
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date_of_order = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    ordered_rooms = models.ManyToManyField(Room)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_of_order)


class User(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    balance = models.IntegerField()

    def __str__(self):
        return self.login
