from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Customer,Employee

class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dob"].label = "Date of Birth"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # if not email.endswith(('@std.neu.edu.tr')):
        #     raise forms.ValidationError('Invalid Student Email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email address already in use.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.dob = self.cleaned_data.get('dob')
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number=self.cleaned_data.get('phone_number')
        customer.location=self.cleaned_data.get('location')
        customer.save()
        return user

class EmployeeSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=True, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dob"].label = "Date of Birth"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith(('@neu.edu.tr')):
            raise forms.ValidationError('Invalid Staff Email')
        elif User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Email address already in use.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.is_staff = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.dob = self.cleaned_data.get('dob')
        user.email = self.cleaned_data.get('email')
        user.save()
        employee = Employee.objects.create(user=user)
        employee.phone_number=self.cleaned_data.get('phone_number')
        employee.designation=self.cleaned_data.get('designation')
        employee.save()
        return user
