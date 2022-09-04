from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login
from .models import Room
from .forms import RegisterForm

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
    return render(request, 'profile.html')


def register(request):
    form = RegisterForm(request.POST)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            # messages.success(request, 'User Created succesfully')
            return redirect('profile')

    return render(request, 'registration/register.html', context)
