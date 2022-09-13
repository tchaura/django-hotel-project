from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, get_user
from django.contrib import messages
from .models import Room, Order, Basket, User
from .forms import RegisterForm
from home.forms import UserLoginForm, RoomsFilterForm
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    total_rooms_number = len(Room.objects.all())
    available_rooms_number = len(Room.objects.filter(status__exact="available"))

    context = {
        "total_rooms_number": total_rooms_number,
        "available_rooms_number": available_rooms_number,
    }

    return render(request, template_name='home.html', context=context)


def filter_form(request):
    form = RoomsFilterForm(request.POST)


    return form


# class RoomsListView(generic.ListView):
#     model = Room
#     context_object_name = 'rooms_list'
#
#     def get_queryset(self):
#         return Room.objects.order_by('number')
#

def rooms(request):

    form = RoomsFilterForm(request.POST)
    room_query_set = Room.objects.all()
    is_found = False
    auth_alert_show = False
    context = {
        'form': form,
        'room_list': room_query_set,
        'is_found' : is_found,
        'auth_alert_show': auth_alert_show,

    }

    if request.method == 'POST' and request.POST.get('findRoom') == 'find':
        if form.is_valid():
            filtered_rooms_query_set = Room.objects.filter(
                capacity__exact=form.cleaned_data['capacity'],
                price__range=[form.cleaned_data['price_from'], form.cleaned_data['price_to']],
            )
            if form.cleaned_data['floor']:
                filtered_rooms_query_set = filtered_rooms_query_set.filter(
                    floor__exact=form.cleaned_data['floor']
                )
            if form.cleaned_data['comfortability'] != 'any':
                filtered_rooms_query_set = filtered_rooms_query_set.filter(
                    comfortability__exact=form.cleaned_data['comfortability']
                )

            room_orders = Order.objects.filter(ordered_rooms__in=filtered_rooms_query_set)
            if room_orders:
                closest_check_out_date = room_orders.filter(check_out_date__lte=form.cleaned_data['date_from']).last()

                closest_check_in_date = room_orders.filter(check_in_date__gte=form.cleaned_data['date_to']).last()
                if closest_check_out_date and closest_check_in_date:
                    print(closest_check_out_date.check_out_date)
                    print(closest_check_in_date.check_in_date)
                    if closest_check_out_date.check_out_date < closest_check_in_date.check_in_date:
                        context['room_list'] = filtered_rooms_query_set
                elif closest_check_out_date:
                    print(closest_check_out_date.check_out_date)
                    if len(Order.objects.all()) > 1:
                        context['room_list'] = Room.objects.none()
                    else:
                        context['room_list'] = filtered_rooms_query_set
                else:
                    context['room_list'] = Room.objects.none()
            else:
                context['room_list'] = Room.objects.none()

            if context['room_list']:
                context['is_found'] = True

            return render(request, template_name='home/room_list.html', context=context)
        else:
            print('form error')

    # if request.method == 'POST' and request.POST.get('orderRoom'):
    #     ordered_room_number = request.POST.get('orderRoom')
    #     form.save()
    #     user = get_user(request)
    #     if user.id:
    #         basket = Basket(customer=user,
    #                         check_in_date=form.cleaned_data['date_from'],
    #                         check_out_date=form.cleaned_data['date_to'],
    #                         ordered_rooms=Room.objects.get(ordered_room_number),
    #                         )
    #         basket.save()
    #         
    #
    #     context['auth_alert_show'] = True
    #     messages.warning(request, "Необходима авторизация")


    return render(request, template_name='home/room_list.html', context=context)


class RoomsDetailView(generic.DetailView):
    model = Room
    context_object_name = "room"


def profile(request):
    return render(request, 'profile.html')


def user_login(request):
    form = UserLoginForm(request.POST)
    context = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            print('success')
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            login(request, user)
            return redirect('profile')
    else:
        for field in form:
            print("Field Error:", field.name, "Error", field.errors)
        print(form.non_field_errors())

    return render(request, 'registration/login.html', context)


def register(request):

    form = RegisterForm(request.POST)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            # messages.success(request, 'User Created successfully')
            return redirect('profile')

    return render(request, 'registration/register.html', context)
