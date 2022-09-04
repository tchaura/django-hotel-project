from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        model = User