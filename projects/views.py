from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from users.models import Users
from .models import *
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg, Sum
from .forms import NewProject, ImageForm, Report
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
    user_rating_count = Project_rating.objects.filter(project_id=id, user_id=user).count()
    project_pics = project.project_pics_set.all()
    comments = Project_comments.objects.filter(project_id=id)
    if user_rating_count:
        user_rating = Project_rating.objects.get(project_id=id, user_id=user).rating
    else:
        user_rating = 0

    if donations["donation__sum"]:
        project_donation = donations["donation__sum"]
        if donations["donation__sum"] >= (project.total_target*0.25):
            donations_flag = 0
        else:
            donations_flag = 1
    else:
        donations_flag = 1
        project_donation = 0
        
    context = {'project': project,
               'donations_flag': donations_flag,
               'user_rate': user_rating,
               'pics': project_pics,
               'donations': project_donation,
               'comments': comments,
               'report_form': Report(),
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
        return redirect(reverse('users:projects'))

# http://127.0.0.1:8000/project/:id/rating/:rate
def project_rating(res, id, rate):
    if res.method == "POST":
        user = res.user.id
        project = Projects.objects.get(id=id)
        Project_rating.objects.update_or_create(project_id=id, user_id=user, defaults={'rating': rate})        
        project_rating = project.project_rating_set.all().aggregate(Avg("rating"))["rating__avg"]
        Projects.objects.update_or_create(id=id,defaults={'rating': project_rating})
        return redirect('project_page', id=id)



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
        return render(request, 'home_page.html', {"NOdata": " your search key word doesn't match any projects !"})


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
            tags = request.POST.getlist('tags')
            form = project_form.save(commit=False)
            form.user = request.user
            form.save()
            for file in request.FILES.getlist('images'):
                Project_pics(project_id=form.id, pic=file).save()

            if request.POST['new_tag']:
                new_tags = request.POST['new_tag'].split(':')
                for new_tag in new_tags:
                    tag = Tags(name=new_tag)
                    tag.save()
                    tags.append(tag.id)
                print(tags)
            for tag_id in tags:
                Project_tags(project_id=form.id, tag_id=tag_id).save()
            return HttpResponseRedirect(reverse("users:projects"))
        else:
            print(project_form.errors)
    else:
        project_form = NewProject()
    return render(request, reverse("users:projects"), {'project_form': project_form, })


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
            print("comment:", comment)
            if len(comment) > 0:
                Project_comments.objects.create(
                    project_id=project_id,
                    comment=comment,
                    user_id=request.user.id
                )
                return redirect(f"/project/{project_id}")
            else:
                return redirect(f"/project/{project_id}")
        except:
            messages.error(request, 'Please login first!!!', extra_tags='comment')
            return redirect(f"/project/{project_id}")
    else:
        return redirect(f"/project/{project_id}")


def report(request, project_id):
    context = {}
    if request.method == 'POST':
        report_form = Report(request.POST)
        if report_form.is_valid():
            new_report = report_form.save(commit=False)
            new_report.user = request.user
            if 'comment' not in request.POST:
                new_report.project = Projects.objects.get(pk=request.POST['project'])
            else:
                new_report.Comment = Project_comments.objects.get(pk=request.POST['comment'])
            new_report.save()
            return HttpResponseRedirect(reverse("projects:project_page", args=[project_id]))
        else:
            print(report_form.errors)
    else:
        report_form = Report()
    context['report_form'] = report_form
    return render(request, reverse("project:project_page"), context)
