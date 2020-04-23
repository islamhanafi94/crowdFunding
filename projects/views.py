from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse,HttpResponseForbidden
from users.models import Users
from .models import *
from django.contrib.auth.models import User
from django.db.models import  Avg, Sum
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

    latestFiveList = Projects.objects.extra(order_by=['-created_at'])
    featuredList = Projects.objects.all().filter(featured='True')
    categories = Categories.objects.all()

    context = {
        'latestFiveList': latestFiveList,
        'featuredList': featuredList,
        'highRatedProjects': highRatedProjects,
        'categories': categories,
        'Ahmed':'Ahmed',
    }
    return render(request, 'home_page.html', context)


