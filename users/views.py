from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from users.forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from users.tokens import account_activation_token
# from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from users.models import Users

# Create your views here.


def test(request):
    context = {'greeting': 'hello'}
    return render(request, 'users/home.html', context)


def register_view(request):
    context = {}
    if request.POST:
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            # user = authenticate(email=email, password=password)
            # login(request, user)

            # send an email to the user with the token

            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
#############################################################################################################################
            return redirect('users')
        else:
            context['form'] = form
    else:
        form = RegistraionForm()
        context['form'] = form
    return render(request, 'users/register.html', context)


def activate(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect(reverse('users:home'))

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('users:home'))

    else:
        form = LoginForm()

    context['form'] = form

    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('users:home'))
