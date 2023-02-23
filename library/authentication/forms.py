from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UsernameField, PasswordChangeForm
from django.forms import ModelForm, Textarea
from .models import CustomUser
from django.core.validators import validate_email

import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class CustomUserModelFormRegister(forms.ModelForm):
    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
        'incorrect_data': "Incorrect data",
    }
    email = forms.CharField(required=True,
                            max_length=80,
                            validators=[validate_email])

    password1 = forms.CharField(
        label="Password",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        required=True,
        # help_text="Enter the same password as before, for verification.",
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'role']
        # field_classes = {"email": UsernameField}


        labels = {
            'email': 'Email!',
        }
        help_texts = {
            # 'email': 'Some useful help text.',
        }
        error_messages = {
            'email': {
                'correct_mail': "This email must be like user@mail.com.",
            },
        }


class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": ("This account is inactive."),
    }


class UpdateUserModelForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput, max_length=30)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
                                label='Confirm password')



    class Meta:
        model = CustomUser
        exclude = ['last_login', 'user_permissions', 'groups']
        # labels = {
        #     'password2': 'Confirm password'
        # }
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')

        return email

    def clean_password2(self):
        confirm_password = self.cleaned_data['password2']
        original_password = self.cleaned_data['password']
        if original_password != confirm_password:
            raise forms.ValidationError("Password doesn't match11")

        return confirm_password

    field_order = ['email', 'password', 'password2']



class ChangePasswordModelForm(PasswordChangeForm):

    # password_old = forms.CharField(widget=forms.PasswordInput, max_length=30,
    #                                label='Provide old password')
    # password = forms.CharField(widget=forms.PasswordInput, max_length=30)
    # password2 = forms.CharField(widget=forms.PasswordInput, max_length=30,
    #                             label='Confirm password')

    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control',
                   'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm password'}),
    )

    def clean_new_password2(self):
        confirm_password = self.cleaned_data['new_password1']
        original_password = self.cleaned_data['new_password2']
        if original_password != confirm_password:
            raise forms.ValidationError("Password doesn't match11")

        return confirm_password