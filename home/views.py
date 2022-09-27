from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, get_user, update_session_auth_hash
from django.contrib import messages
from .models import Room, Order, Basket, User
from .forms import RegisterForm, NameEditForm
from home.forms import UserLoginForm, RoomsFilterForm
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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

    context = {
        'form': form,
        'room_list': room_query_set,
        'is_found': is_found,

    }

    if request.method == 'POST' and request.POST.get('findRoom') == 'find':

        if form.is_valid():

            basket = Basket(
                date_from=form.cleaned_data['date_from'],
                date_to=form.cleaned_data['date_to']
            )
            basket.save()

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
                closest_check_out_date = room_orders.filter(check_out_date__lte=form.cleaned_data['date_to']).last()

                closest_check_in_date = room_orders.filter(check_in_date__gte=form.cleaned_data['date_from']).last()

                if closest_check_out_date and closest_check_in_date:
                    print("Check-in date" + str(closest_check_in_date.check_in_date))
                    print("Check-out date" + str(closest_check_out_date.check_out_date))
                    if closest_check_out_date.check_out_date < closest_check_in_date.check_in_date:
                        context['room_list'] = filtered_rooms_query_set
                        context['is_found'] = True
                    else:
                        context['room_list'] = Room.objects.none()
                elif closest_check_out_date:
                    print("Check-out date" + str(closest_check_out_date.check_out_date))
                    if len(Order.objects.all()) == 1:
                        context['room_list'] = Room.objects.none()
                    else:
                        context['room_list'] = filtered_rooms_query_set
                        context['is_found'] = True
                else:
                    context['room_list'] = Room.objects.none()
            else:
                context['room_list'] = Room.objects.none()

            # if context['room_list']:
            #     context['is_found'] = True

            return render(request, template_name='home/room_list.html', context=context)
        else:
            print('form error')

    if request.method == 'POST' and request.POST.get('orderRoom'):
        ordered_room_number = request.POST.get('orderRoom')

        basket = Basket.objects.first()
        date_from = basket.date_from
        date_to = basket.date_to
        user = get_user(request)
        if user.id:
            order = Order(customer=user,
                          check_in_date=date_from,
                          check_out_date=date_to,
                          ordered_rooms=Room.objects.get(number__exact=ordered_room_number),
                          )
            order.save()
            print('order saved')
            Basket.delete(Basket.objects.first())
            messages.success(request, "Ваш заказ успешно создан", extra_tags='order_created')

        else:
            messages.warning(request, "Для заказа комнаты вам необходимо авторизоваться", extra_tags='authorize')


    return render(request, template_name='home/room_list.html', context=context)


class RoomsDetailView(generic.DetailView):
    model = Room
    context_object_name = "room"


def profile(request):
    if request.user.is_authenticated:
        user = get_user(request)
        name_edit_form = NameEditForm(request.POST, instance=request.user)
        password_change_form = PasswordChangeForm(request.user, request.POST)
        user_orders = Order.objects.filter(customer=user.id)
        context = {
            'current_user': user,
            'user_orders': user_orders
        }
    else:
        context = {}

    if request.method == 'POST' and request.POST.get('editName') == 'edit':
        context['name_edit_form'] = name_edit_form
        return render(request, 'profile.html', context)

    if request.method == 'POST' and request.POST.get('saveName') == 'submit':
        if name_edit_form.is_valid():
            name_edit_form.save()
        return render(request, 'profile.html', context)

    if request.POST.get('changePassword'):
        context['password_change_form'] = password_change_form

    if request.POST.get('savePassword'):
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль был успешно изменен', extra_tags='password_change_successful')
        else:
            if password_change_form.has_error('old_password'):
                messages.error(request, 'Старый пароль неверен', extra_tags='password_error')
            if password_change_form.has_error('new_password1'):
                messages.error(request, 'Новый пароль не подходит по критериям', extra_tags='password_error')
            if password_change_form.has_error('new_password2'):
                messages.error(request, 'Пароли не совпадают', extra_tags='password_error')

    if request.POST.get('deleteOrder'):
        order_id = request.POST.get('deleteOrder')
        order_to_delete = Order.objects.filter(id=order_id)
        order_to_delete.delete()
        messages.success(request, 'Заказ успешно удален', extra_tags='order_delete_successful')

    return render(request, 'profile.html', context)


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

def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = ""
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html", context={"password_reset_form":password_reset_form})


def about(request):
    return render(request, 'about.html')