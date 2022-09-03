from django.shortcuts import render
from django.views import generic

from .models import Room, UserProfile
# Create your views here.


def index(request):
    total_rooms_number = len(Room.objects.all())
    available_rooms_number = len(Room.objects.filter(status__exact="available"))

    context = {
        "total_rooms_number": total_rooms_number,
        "available_rooms_number": available_rooms_number,
    }

    return render(request, template_name='home.html', context=context)

class RoomsListView(generic.ListView):
    model = Room
    context_object_name = 'rooms_list'

    def get_queryset(self):
        return Room.objects.order_by('number')


class RoomsDetailView(generic.DetailView):
    model = Room
    context_object_name = "room"


def profile(request):
    user = UserProfile.user

    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)