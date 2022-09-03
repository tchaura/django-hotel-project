from django.contrib import admin
from .models import Room, UserProfile, Order
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = "login", "name", "surname", "balance"
#

class OrderInline(admin.TabularInline):
    model = Order.ordered_rooms.through


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = "number", "floor", "price", "comfortability", "capacity", "status"

    inlines = [OrderInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "customer", "check_in_date", "check_out_date"

    inlines = [OrderInline]
    exclude = ('ordered_rooms',)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


