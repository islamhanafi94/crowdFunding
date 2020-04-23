from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse,HttpResponseForbidden
from users.models import Users
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Sum
# Create your views here.
# Create your views here.

# http://127.0.0.1:8000/project/home
# I Want to make this render the tamplate that in the root 
def home(request):
    projectRates = Rating.objects.all().values('project').annotate(
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


def search(request):
    if request.GET.get("search"):
        search_keyword = request.GET.get("search")
        # search_set = Projects.objects.filter(Q(title__icontains = search_keyword)|Q(project_tags__name__icontains = search_keyword)).distinct()
        search_set = Projects.objects.filter(Q(title__icontains = search_keyword))
        search_set2=Project_tags.objects.filter(Q(tag__name__icontains = search_keyword)).distinct()
        #search_set = Project.objects.filter(tages__name__startswith = search_keyword)
        picture = []

        for p in search_set:
            picture.extend(
                list(Project_pics.objects.filter(id= p.pk )))
        context = {
            "projects_search": search_set,
            "projects_search2": search_set2,
            'picture':picture

        }
        return render(request, 'home_page.html', context)

    else:
         return render(request, 'home_page.html', context)

