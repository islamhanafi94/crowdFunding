from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden
from users.models import Users
from .models import *
from django.contrib.auth.models import User
from django.db.models import Avg, Sum
import datetime
from django.contrib import messages


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
        'categories': categories
    }
    return render(request, 'projects/home.html', context)


def project(request, project_id):
    images = []
    try:
        project = Projects.objects.get(id=project_id)
        pics = Project_pics.objects.filter(project_id=project_id)
        for i in pics:
            pics.append(i.pic)
        project_all_tags = Project_tags.objects.filter(
            project_id=project_id).values_list("tag", flat=True)
        test_list = list(project_all_tags)
        related_projects_id = Project_tags.objects.filter(tag__in=test_list).distinct(
        ).exclude(project_id=project_id).values_list("project", flat=True)[:5]
        related_projects_data = Projects.objects.filter(
            id__in=list(related_projects_id))

        # get project comments
        comments = Project_comments.objects.filter(project_id=project_id)
        if 'logged_in_user' in request.session:
            if request.session['logged_in_user'] == project.user_id:
                project_owner = True
            else:
                project_owner = False
        else:
            project_owner = False

        is_ended = True if project.end_date < datetime.date.today() else False

        is_completed = True if project.current_money >= project.target else False
        context = {
            "pics": images,
            "Projects": project,
            "comments": comments,
            "related_projects_list": related_projects_data,
            "owner": project_owner,
            "is_ended": is_ended,
            "is_completed": is_completed
        }

    except Projects.DoesNotExist:
        return redirect(f'/project/error')
    return render(request, 'projects/project.html', context)


def donate(request, project_id):
    if request.method == 'POST':
        try:
            donating_value = int(request.POST.get('donation_value'))
            project = Projects.objects.get(id=project_id)
            project.current_money += donating_value
            if project.current_money <= project.target:
                project.save()
                Project_donations.objects.create(
                    project=project,
                    user=Users.objects.get(user_id=request.session['logged_in_user']),
                    value=donating_value
                )
                messages.success(request, 'Your Donation done successfully!', extra_tags='donate')
                return redirect(f"/project/{project_id}")
            else:
                messages.error(request, 'Your Donation failed', extra_tags='donate')
                return redirect(f"/project/{project_id}")
        except:
            messages.error(request, 'Please login first!!!', extra_tags='donate')
            return redirect(f"/project/{project_id}")
    else:
        return redirect(f"/project/{project_id}")


def comment(request, project_id):
    if request.method == 'POST':
        try:
            project = Projects.objects.get(id=project_id)
            comment = request.POST.get('comment')
            if len(comment) > 0:
                Project_comments.objects.create(
                    project=project,
                    comment=comment,
                    comment_user_id=request.session['logged_in_user']
                )
                return redirect(f"/project/{project_id}")
            else:
                return redirect(f"/project/{project_id}")
        except:
            messages.error(request, 'Please login first!!!', extra_tags='comment')
            return redirect(f"/project/{project_id}")
    else:
        return redirect(f"/project/{project_id}")
