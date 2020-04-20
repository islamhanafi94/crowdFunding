from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from users.forms import *
from django.http import HttpResponse


# Create your views here.


def test(request):
    context = {'greeting': 'hello'}
    return render(request, 'users/test.html', context)



def register_view(request):
    context = {}
    if request.POST:
        form = RegistraionForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(email=email, password=password)
            # login(request, user)
            return  redirect('users')
        else:
            context['form'] = form
    else:
        form = RegistraionForm()
        context['form'] = form
    return render(request, 'users/register.html', context)



def sucess(request):
    return HttpResponse('successfully uploaded')