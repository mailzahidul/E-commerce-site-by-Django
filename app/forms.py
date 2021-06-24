from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, Mulytic_labs_test


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'})
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current_password','class':'form-control'}))


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user',]
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'district':forms.Select(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label="Confirm New Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))


class MulyticForm(forms.ModelForm):
    class Meta:
        model = Mulytic_labs_test
        exclude = ['order_time', 'qr_code']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder':'+8801919100108','class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'product': forms.Select(attrs={'class':' product_code form-control'}),
            'quantity': forms.TextInput(attrs={'class':'quantity form-control '}),
            'payment_method': forms.Select(attrs={'label':'Payment Method','class':'quantity form-control '}),
        }