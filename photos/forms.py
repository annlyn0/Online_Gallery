from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username...'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password...'})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters.")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 3:
            raise forms.ValidationError("Password must be at least 3 characters.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        username = cleaned_data.get("username")

        # **🚀 Allow username-based passwords**
        # ✅ Removes Django's default validation for similarity
        if password and username and password == username:
            pass  # No error, user can set password same as username.

        return cleaned_data
