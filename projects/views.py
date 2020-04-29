from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from users.models import Users
from .models import *
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg, Sum
from .forms import NewProject, ImageForm
from django.forms import modelformset_factory
from django.contrib import messages


# Create your views here.
# Create your views here.

# http://127.0.0.1:8000/project/home
# I Want to make this render the tamplate that in the root


def home(request):
    projectRates = Project_rating.objects.all().values('project').annotate(
        Avg('rating')).order_by('-rating__avg')[:5]
    print(projectRates)

    highRatedProjects = []
    for p in projectRates:
        print(p.get('project'))
        highRatedProjects.extend(
            list(Projects.objects.filter(id=p.get('project'))))
        print(highRatedProjects)

    latestFiveList = Projects.objects.extra(order_by=['-created_at'])[:5]
    featuredList = Projects.objects.all().filter(featured='True')[:5]
    categories = Categories.objects.all()
    context = {
        'latestFiveList': latestFiveList,
        'featuredList': featuredList,
        'highRatedProjects': highRatedProjects,
        'categories': categories,
    }
    return render(request, 'home_page.html', context)


# http://127.0.0.1:8000/project/:id


def project_page(res, id):
    project = Projects.objects.get(id=id)
    user = res.user.id
    donations = project.project_donations_set.all().aggregate(Sum("donation"))
    user_rating_count = Project_rating.objects.filter(
        project_id=id, user_id=user).count()
    if user_rating_count:
        user_rating = Project_rating.objects.get(
            project_id=id, user_id=user).rating
    else:
        user_rating = 0
    if donations["donation__sum"]:
        if donations["donation__sum"] >= (project.total_target*0.25):
            donations_flag = 0
        else:
            donations_flag = 1
    else:
        donations_flag = 1

    context = {'project': project,
               'donations_flag': donations_flag,
               'user_rate': user_rating
               }

    return render(res, 'projects/project_page.html', context)


# http://127.0.0.1:8000/project/:id/cancel


def cancel_project(res, id):
    if res.method == "POST":
        user = res.user.id
        project = Projects.objects.get(id=id, user_id=user)
        if not project:
            raise HttpResponseForbidden("Not Authorized")
        project.delete()
        # return render(res, 'projects/test_page.html', {'test' : "canceled"} )
        return redirect(reverse('users:projects'))

# http://127.0.0.1:8000/project/:id/rating/:rate


def project_rating(res, id, rate):
    if res.method == "POST":
        user = res.user.id
        project = Projects.objects.get(id=id)
        Project_rating.objects.update_or_create(
            project_id=id, user_id=user, rating=rate)
        project_rating = project.project_rating_set.all().aggregate(Avg("rating"))[
            "rating__avg"]
        project_rating = Decimal(project_rating).quantize(0, ROUND_HALF_UP)
        project.update_or_create(rating=project_rating)
        return render(res, 'projects/test_page.html', {'test': "rated"})


def search(request):
    if request.GET.get("search"):
        res = []
        search_keyword = request.GET.get("search")
        search_tag_counter = Tags.objects.filter(name=search_keyword).count()
        if search_tag_counter:
            search_tag = Tags.objects.get(name=search_keyword)
            search_set = Project_tags.objects.filter(tag_id=search_tag.id)
            for project in search_set:
                res.append(Projects.objects.get(id=project.project_id))
        elif search_tag_counter == 0:
            res = Projects.objects.filter(title=search_keyword)
        else:
            res = ["No res"]
        context = {
            "projects_search": res
        }
        return render(request, 'home_page.html', context)
    else:
        return render(request, 'home_page.html', {"NOdata": "There is No such a tag or title matched our projects Plz try Again"})


def showCategoryProjects(request, cat_id):
    c = get_object_or_404(Categories, pk=cat_id)
    category_projects = c.projects_set.all()
    context = {
        'category_name': c.title,
        'category_projects': category_projects
    }
    return render(request, "viewCategory.html", context)


def create_project(request):
    if request.method == 'POST':
        project_form = NewProject(request.POST)
        if project_form.is_valid():
            form = project_form.save(commit=False)
            form.user = request.user
            form.save()
            for file in request.FILES.getlist('images'):
                project_pic = Project_pics(project_id=form.id, pic=file).save()
            return HttpResponseRedirect(reverse("users:projects"))
        else:
            print(project_form.errors)
    else:
        project_form = NewProject()
    return render(request, reverse("users:projects"), {'project_form': project_form, })
