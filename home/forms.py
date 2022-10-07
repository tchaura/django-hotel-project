import datetime

import django.contrib.auth.forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth import get_user, password_validation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from crispy_forms.bootstrap import StrictButton
from django.core.exceptions import ValidationError

from .models import Basket


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-loginForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.form_show_labels = True
        self.fields['username'].required = True
        self.fields['password'].required = True
        self.helper.layout = Layout(
            'username',
            'password',
        )
        self.helper.add_input(Submit('login', 'Войти', css_class = 'btn-primary'))


class RegisterForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        model = User

    # use_required_attribute = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )
        self.helper.error_text_inline = True
        self.helper.form_show_errors = True
        self.helper.add_input(Submit('register', 'Зарегистрироваться'))


class RoomsFilterForm(forms.Form):
    CAPACITY_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    ]

    date_from = forms.DateField(label='Дата заселения', widget=forms.TextInput({'type': 'date'}))
    date_to = forms.DateField(label='Дата выселения', widget=forms.TextInput({'type': 'date'}))
    capacity = forms.ChoiceField(label='Вместимость', choices=CAPACITY_CHOICES, initial=CAPACITY_CHOICES[0])

    def clean(self):
        cd = self.cleaned_data

        if cd.get('date_to') and cd.get('date_from'):
            if cd.get('date_to') <= cd.get('date_from'):
                self.add_error('date_to', 'Дата выселения должна быть позднее, чем дата заселения')
            if cd.get('date_from') < datetime.date.today():
                # raise ValidationError('Date must be equal or greater than today')
                self.add_error('date_from', 'Дата заселения должна быть не ранее текущей даты')

        return cd


class NameEditForm(forms.ModelForm):
    #
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    # def clean(self):
    #     cd = self.cleaned_data
    #
    #     if not cd.get('first_name'):
    #         self.add_error('first_name', 'Имя не должно быть пустым')
    #
    #     if not cd.get('last_name'):
    #         self.add_error('last_name', 'Фамилия не должна быть пустой')
    #
    #     return cd


class CustomPasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].required = True
        # self.fields['username'].required = True
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-passwordChangeForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit'
        # self.helper.layout = Layout(
        #     'first_name',
        #     'last_name',
        #     'email',
        #     'username',
        #     'password1',
        #     'password2',
        # )
        self.helper.error_text_inline = True
        self.helper.form_show_errors = True
        self.helper.add_input(Submit('submit', 'Изменить'))
