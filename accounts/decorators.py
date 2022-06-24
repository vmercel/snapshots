from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
#new
from .models import User

def unauthenticated_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_customer:
                return HttpResponseRedirect(reverse('dashboard-index'))
            elif request.user.is_employee:
                return HttpResponseRedirect(reverse('dashboard-index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrap


def student_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_customer:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('dashboard-index'))
    return wrap


def lecturer_only(view_func):
    # def wrap(request, *args, **kwargs):
    #     return view_func(request, *args, **kwargs)
    # return wrap
    def wrap(request, *args, **kwargs):
        if request.user.is_employee:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

