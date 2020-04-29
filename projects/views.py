from django.shortcuts import render, redirect, get_object_or_404
<<<<<<< HEAD
from django.http.response import HttpResponse, JsonResponse, HttpResponseForbidden
from users.models import Users
from .models import *
from django.contrib.auth.models import User

from django.db.models import Avg, Sum
import datetime
from django.contrib import messages

from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg, Sum
=======
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
>>>>>>> 94fdfba508224b68b363c4cd972ea94e787bb4c7


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
<<<<<<< HEAD
    user_rating = project.project_rating_set.get(user_id=user).rating
    if donations["donation__sum"] >= (project.total_target * 0.25):
        donations_flag = 0
    else:
        donations_flag = 1
    context = {'project': project,
               'donations_flag': donations_flag,
               'user_rate': Decimal(user_rating).quantize(0, ROUND_HALF_UP)
               }
=======
    user_rating_count = Project_rating.objects.filter(project_id=id, user_id=user).count()
    if user_rating_count:
        user_rating = Project_rating.objects.get(project_id=id, user_id=user).rating
    else:
        user_rating = 0
    if donations["donation__sum"]:
        if donations["donation__sum"] >= (project.total_target*0.25):
            donations_flag = 0
        else:
            donations_flag = 1
    else:
        donations_flag = 1

    context = { 'project': project,
                'donations_flag' : donations_flag,
                'user_rate' : user_rating
            }

>>>>>>> 94fdfba508224b68b363c4cd972ea94e787bb4c7
    return render(res, 'projects/project_page.html', context)


# http://127.0.0.1:8000/project/:id/cancel
def cancel_project(res, id):
    if res.method == "POST":
        user = res.user.id
        project = Projects.objects.get(id=id, user_id=user)
        if not project:
            raise HttpResponseForbidden("Not Authorized")
        project.delete()
        return render(res, 'projects/test_page.html', {'test': "canceled"})
<<<<<<< HEAD
=======

>>>>>>> 94fdfba508224b68b363c4cd972ea94e787bb4c7


def project_rating(res, id, rate):
    if res.method == "POST":
        user = res.user.id
        project = Projects.objects.get(id=id)
        Project_rating.objects.update_or_create(project_id=id, user_id=user, rating=rate)
        project_rating = project.project_rating_set.all().aggregate(Avg("rating"))["rating__avg"]
        project_rating = Decimal(project_rating).quantize(0, ROUND_HALF_UP)
        project.update_or_create(rating=project_rating)
<<<<<<< HEAD
        return render(res, 'projects/test_page.html', {'test': "rated"})
=======
        return render(res, 'projects/test_page.html', {'test' : "rated"})
>>>>>>> 94fdfba508224b68b363c4cd972ea94e787bb4c7


def search(request):
    if request.GET.get("search"):
        res = []
        search_keyword = request.GET.get("search")
<<<<<<< HEAD
        search_set = Projects.objects.filter(
            Q(title__icontains=search_keyword) | Q(tags__name__icontains=search_keyword)).distinct()
=======
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
>>>>>>> 94fdfba508224b68b363c4cd972ea94e787bb4c7
        context = {
            "projects_search" : res
        }
        return render(request, 'home_page.html', context)
    else:
        return render(request, 'home_page.html',
                      {"NOdata": "There is No such a tag or title matched our projects Plz try Again"})


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
    return render(request, 'projects/project_page.html', context)


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
