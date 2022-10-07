import random

from django.contrib import admin
from .models import Room, Order
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = "login", "name", "surname", "balance"
#

# class OrderInline(admin.TabularInline):
#     model = Order.ordered_rooms.through
#

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = "number", "floor", "price", "comfortability", "capacity"

    # inlines = [OrderInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "customer", "check_in_date", "check_out_date", "ordered_rooms"

    # inlines = [OrderInline]


# class UserProfileInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = 'user'
#

# class UserAdmin(BaseUserAdmin):
#     inlines = (UserProfileInline,)


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

#
# for i in range(10):
#     room = Room(
#         capacity=random.randint(1, 5),
#         comfortability=Room.COMFORTABILITY_CHOICES[random.randint(0, 2)][0],
#         number=random.randint(2, 320),
#         floor=random.randint(1, 10),
#         price=random.randint(30, 70)
#
#     )
#     room.save()
#
