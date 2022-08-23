from django.contrib import admin
from .models import Room, User, Order


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = "login", "name", "surname", "balance"


class OrderInline(admin.TabularInline):
    model = Order.ordered_rooms.through


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = "number", "floor", "price", "comfortability", "capacity"

    inlines = [OrderInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "user", "check_in_date", "check_out_date"

    inlines = [OrderInline]
    exclude = ('ordered_rooms',)



