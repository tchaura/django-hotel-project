from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from crispy_forms.bootstrap import StrictButton


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-loginForm'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
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

    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'id-loginForm'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = 'login'
    #     self.fields['username'].required = True
    #     self.fields['password'].required = True
    #     self.helper.add_input(Submit('submit', 'Войти'))
    #     self.helper.layout = Layout(
    #         'username',
    #         'password',
    #         'email'
    #     )


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.layout = Layout(
            'username',
            'password',

            # StrictButton('Зарегистрироваться', css_class='btn btn-primary')
        )
        self.helper.error_text_inline = True
        self.helper.form_show_errors = True
        self.helper.add_input(Submit('login', 'Войти'))


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
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
            # StrictButton('Зарегистрироваться', css_class='btn btn-primary')
        )
        self.helper.error_text_inline = True
        self.helper.form_show_errors = True
        self.helper.add_input(Submit('register', 'Зарегистрироваться'))
