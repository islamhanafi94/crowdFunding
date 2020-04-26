from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistraionForm, LoginForm , UpdateUserForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.models import Users
import datetime
from projects.models import Categories, Projects, Project_donations
from projects.forms import NewProject

# Create your views here.


def test(request):
    return HttpResponse("Should route to web app home page")
    # return render(request, "users/home.html", context)


def register_view(request):
    context = {}
    if request.POST:
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_email(user, get_current_site(request),
                       form.cleaned_data.get("email"))
            return HttpResponse(
                "Please confirm your email address to complete the registration"
            )

        else:
            context["form"] = form
    else:
        form = RegistraionForm()
        context["form"] = form
    return render(request, "users/register.html", context)


def activate(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        if user.is_active == False:
            date_joined = user.date_joined.replace(tzinfo=None)
            date_diffrince = (datetime.datetime.now() -
                              date_joined).seconds / 60

            if date_diffrince < (60*24):
                user.is_active = True
                user.save()
                return HttpResponse(
                    "Thank you for your email confirmation. Now you can login your account."
                )
            else:
                current_site = get_current_site(request)
                email = user.email
                send_email(user, current_site, email)
                user.date_joined = datetime.datetime.now()
                user.save()
                return HttpResponse("activation link is valid for five minutes only...")
        else:
            return HttpResponse("Activation link is invalid!")
    else:
        return HttpResponse("Activation link is invalid!")


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        # return redirect(reverse("users:home"))
        return redirect('home_page')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                # return redirect(reverse("users:home"))
                return redirect('home_page')

    else:
        form = LoginForm()

    context["form"] = form

    return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    # return redirect(reverse("users:home"))
    return redirect('home_page')


def send_email(user, current_site, email):
    mail_subject = "Activate your account."
    message = render_to_string(
        "users/acc_active_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def list_projects(request):
    # get all categories
    categories_list = Categories.objects.all()
    # get users's projects
    user_projects = Projects.objects.filter(user_id=request.user.id)

    project_form = NewProject()
    context = {"categories_list": categories_list,
               "user_projects": user_projects,
               "project_form": project_form,
               }

    return render(request, 'users/projects.html', context=context)


def donations_list(request):

    user_donations = Project_donations.objects.filter(user_id=request.user.id)

    context = {"user_donations": user_donations}
    return render(request, 'users/donations.html', context=context)



def user_profile_update(request):
    form = UpdateUserForm(request.POST,request.FILES,instance=request.user)
    if request.POST:
        if form.is_valid():
            print("photo from form is :",form.cleaned_data['photo'])
            form.save()
    else :
        form = UpdateUserForm(
            initial= {
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'phone':request.user.phone,
                'date birth':request.user.date_birth,
                'facebook_link':request.user.facebook_link,
                'country':request.user.country
            }
        )
    context = {'form' : form}
    return render(request , 'users/user_profile_update.html',context=context)


def user_profile(request):
    context = {}
    return render(request , 'users/user_profile.html',context=context)