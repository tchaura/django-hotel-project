

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

def is_greater_than_zero(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is smaller than zero'),
            params={'value': value},
        )

class Room(models.Model):
    capacity = models.IntegerField()
    COMFORTABILITY_CHOICES = [
        ("lux", "Люкс"),
        ("semi-lux", "Полу-люкс"),
        ("standard", "Обычный"),
    ]
    comfortability = models.CharField(choices=COMFORTABILITY_CHOICES, max_length=20)
    number = models.IntegerField(primary_key=True, unique=True)
    floor = models.IntegerField()
    price = models.IntegerField()

    STATUSES_LIST = [
        ("available", "Свободна"),
        ("taken", "Занята"),
    ]

    status = models.CharField(max_length=20, choices=STATUSES_LIST, default=STATUSES_LIST[0])

    def __str__(self):
        return f"Room number {self.number}"

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.number)])


class Order(models.Model):
    timezone.activate('Europe/Minsk')
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    date_of_order = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    ordered_rooms = models.ManyToManyField(Room)
    # user = models.ForeignKey("User", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.date_of_order)


# class UserProfile(models.Model):
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4())
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     patronymic = models.CharField(max_length=20)
#     balance = models.IntegerField(default=0, validators=[is_greater_than_zero])
#
#     # @receiver(post_save, sender=User)
#     # def create_user_profile(sender, instance, created, **kwargs):
#     #     if created:
#     #         UserProfile.objects.create(user=instance)
#     #
#     # @receiver(post_save, sender=User)
#     # def save_user_profile(sender, instance, **kwargs):
#     #     instance.userprofile.save()
