from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistraionForm, LoginForm, UpdateUserForm
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
from projects.models import Categories, Projects, Project_donations, Tags
from projects.forms import NewProject
from django.db.models import Q, Avg, Sum
from django.template.defaulttags import register

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
            send_email(
                user,
                get_current_site(request),
                form.cleaned_data.get("email"),
                "users/acc_active_email.html",
                "Activate your account.",
            )
            return render(request, "users/signup_link_email.html", {"active_code": -1})
        else:
            context["form"] = form
    else:
        form = RegistraionForm()
        context["form"] = form
    return render(request, "users/register.html", context)


def activate(request, uidb64, time):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("user id : ", uid)
        time_sent = force_text(urlsafe_base64_decode(time))
        user = Users.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        if user.is_active == False:
            email_sent_at = time_sent
            date_diffrince = (
                datetime.datetime.now()
                - datetime.datetime.strptime(email_sent_at,
                                             "%Y-%m-%d %H:%M:%S.%f")
            ).seconds / 60

            if date_diffrince < (24 * 60):
                user.is_active = True
                user.save()
                return render(
                    request, "users/signup_link_email.html", {"active_code": 1}
                )
            else:
                current_site = get_current_site(request)
                email = user.email
                send_email(
                    user,
                    current_site,
                    email,
                    "users/acc_active_email.html",
                    "Activate your account.",
                )
                return render(
                    request, "users/signup_link_email.html", {"active_code": 0}
                )
        else:
            return render(request, "users/signup_link_email.html", {"active_code": 2})
    else:
        return render(request, "users/signup_link_email.html", {"active_code": 3})


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("home_page")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("home_page")

    else:
        form = LoginForm()

    context["form"] = form

    return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home_page")


def send_email(user, current_site, email, email_body, email_subject):
    mail_subject = email_subject
    message = render_to_string(
        email_body,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "time": urlsafe_base64_encode(force_bytes(datetime.datetime.now())),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def list_projects(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))
    # get all categories
    # categories_list = Categories.objects.all()
    # get users's projects
    tags = Tags.objects.all()
    user_projects = Projects.objects.filter(user_id=request.user.id)

    donations_flag = {}
    donations = {}
    for project in user_projects:
        donation = project.project_donations_set.all().count()
        total_raised = 0
        don_flag = 1

        if donation:
            total_raised = project.project_donations_set.all(
            ).aggregate(Sum("donation"))["donation__sum"]

            if total_raised >= (project.total_target*0.25):
                don_flag = 0
        donations_flag[project.id] = don_flag
        donations[project.id] = total_raised

    project_form = NewProject()
    context = {"user_projects": user_projects,
               "project_form": project_form,
               "donations": donations,
               "donations_flag": donations_flag,
               "tags": tags,
               }

    return render(request, "users/projects.html", context=context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def donations_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))

    user_donations = Project_donations.objects.filter(user_id=request.user.id)

    context = {"user_donations": user_donations}
    return render(request, "users/donations.html", context=context)


def user_profile_update(request):
    form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
    if request.POST:
        if form.is_valid():
            print("photo from form is :", form.cleaned_data["photo"])
            request.user.photo = form.cleaned_data["photo"]
            form.save()
            return redirect(reverse("users:profile"))
    else:
        form = UpdateUserForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone": request.user.phone,
                "date_birth": request.user.date_birth,
                "facebook_link": request.user.facebook_link,
                "country": request.user.country,
            }
        )
    context = {"form": form}
    return render(request, "users/user_profile_update.html", context=context)


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))
    return render(request, "users/user_profile.html")


def send_delete_email(request):
    user = request.user
    current_site = get_current_site(request)
    email = user.email
    email_subject = "Delete your account"
    email_body = "users/acc_del_email.html"
    send_email(user, current_site, email, email_body, email_subject)
    return render(request, "users/delete_account_email.html", {"delete_code": -1})


def delete_account(request, uidb64, time):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        time_sent = force_text(urlsafe_base64_decode(time))
        user = Users.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        email_sent_at = time_sent
        date_diffrince = (
            datetime.datetime.now()
            - datetime.datetime.strptime(email_sent_at, "%Y-%m-%d %H:%M:%S.%f")
        ).seconds / 60

        if date_diffrince < (24 * 60):
            user.delete()
            logout(request)
            return render(
                request, "users/delete_account_email.html", {"delete_code": 1}
            )
        else:
            current_site = get_current_site(request)
            email = user.email
            send_email(
                user,
                current_site,
                email,
                "users/acc_del_email.html",
                "Delete your account.",
            )
            return render(
                request, "users/delete_account_email.html", {"delete_code": 0}
            )
    else:
        return render(request, "users/delete_account_email.html", {"delete_code": 2})
