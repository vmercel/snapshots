from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import CustomerSignUpForm, EmployeeSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .decorators import unauthenticated_user

@unauthenticated_user
def index(request):
    context = {}
    return render(request, '../templates/accounts/indexnew.html', context)

@unauthenticated_user
def register(request):
    return render(request, '../templates/accounts/register.html')

# @unauthenticated_user
class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = '../templates/accounts/customer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

# @unauthenticated_user
class employee_register(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = '../templates/accounts/employee_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

from django.http import HttpResponseRedirect
from django.urls import reverse

@unauthenticated_user
def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard-index'))
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/accounts/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')
