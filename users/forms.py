from django import forms


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput(), min_length=8, max_length=36)
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=8, max_length=36)

