from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse,HttpResponseForbidden
from users.models import Users
from .models import *
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP 
from django.db.models import Q, Avg, Sum
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
    user_rating = project.project_rating_set.get(user_id=user).rating
    if donations["donation__sum"] >= (project.total_target*0.25):
        donations_flag = 0
    else:
        donations_flag = 1
    context = { 'project': project,
                'donations_flag' : donations_flag,
                'user_rate' : Decimal(user_rating).quantize(0, ROUND_HALF_UP)
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
        return render(res, 'projects/test_page.html', {'test' : "canceled"} )


def project_rating(res, id, rate):
    if res.method == "POST":
        user = res.user.id
        project = Projects.objects.get(id=id)
        Project_rating.objects.update_or_create(project_id=id, user_id=user, rating=rate)
        project_rating = project.project_rating_set.all().aggregate(Avg("rating"))["rating__avg"]
        project_rating = Decimal(project_rating).quantize(0, ROUND_HALF_UP)
        project.update_or_create(rating=project_rating)
        return render(res, 'projects/test_page.html', {'test' : "rated"})
def search(request):
    if request.GET.get("search"):
        search_keyword = request.GET.get("search")
        # search_set = Projects.objects.filter(Q(title__icontains = search_keyword)|Q(project_tags__name__icontains = search_keyword)).distinct()
        search_set = Projects.objects.filter(Q(title__icontains = search_keyword))
        search_set2=Project_tags.objects.filter(Q(tag__name__icontains = search_keyword)).distinct()
        #search_set = Project.objects.filter(tages__name__startswith = search_keyword)
        context = {
            "projects_search": search_set,
            "projects_search2": search_set2,

        }
        return render(request, 'home_page.html', context)

    else:
         return render(request, 'home_page.html', context)
def showPic(request,id):
        pic=Project_pics.objects.all().filter(project_id=id)
        context={
            'picture':pic

        }
        return render(request, 'home_page.html', context)

    


def showCategoryProjects(request, cat_id):
    c = get_object_or_404(Categories, pk=cat_id)
    category_projects = c.projects_set.all()
    context = {
        'category_name': c.title,
        'category_projects': category_projects
    }
    return render(request, "viewCategory.html", context)
