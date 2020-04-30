from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.core.exceptions import *
from django.core.exceptions import ObjectDoesNotExist

from django.template.defaulttags import register

from users.models import Users
from .models import *
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg, Sum
from .forms import NewProject, ImageForm, Report, Donate
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
    project_pics2 = {}
    for p in projectRates:

        # project_pics = p.p_pics_set.all()
        print("id ?? ", p.get('project'))
        highRatedProjects.extend(
            list(Projects.objects.filter(id=p.get('project'))))
        print(highRatedProjects)
        project_pics = Project_pics.objects.filter(project=p.get('project'))
        project_pics2[p.get('project')] = project_pics[0]
        print("project_pics2")

        print(project_pics2)

    latestFiveList = Projects.objects.extra(order_by=['-created_at'])[:5]
    for p in latestFiveList:
        project_pics = Project_pics.objects.filter(project=p.id)
        project_pics2[p.id] = project_pics[0]

    featuredList = Projects.objects.all().filter(featured='True').extra(order_by=['-updated_at'])[:5]
    for p in featuredList:
        project_pics = Project_pics.objects.filter(project=p.id)
        project_pics2[p.id] = project_pics[0]
    categories = Categories.objects.all()
    context = {
        'latestFiveList': latestFiveList,
        'featuredList': featuredList,
        'highRatedProjects': highRatedProjects,
        'categories': categories,
        'pics': project_pics2

    }
    return render(request, 'home_page.html', context)


# http://127.0.0.1:8000/project/:id
def project_page(res, id):
    project = Projects.objects.get(id=id)
    user = res.user.id
    donations = project.project_donations_set.all().aggregate(Sum("donation"))
    user_rating_count = Project_rating.objects.filter(
        project_id=id, user_id=user).count()
    project_pics = project.project_pics_set.all()
    comments = Project_comments.objects.filter(project_id=id)
    if user_rating_count:
        user_rating = Project_rating.objects.get(
            project_id=id, user_id=user).rating
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

    tags = Project_tags.objects.filter(project_id=id)
    projects = []
    for tag in tags:
        p = Project_tags.objects.filter(tag_id=tag.tag_id).exclude(project_id = id)
        if p :
            projects.append(p)
    print(projects)

    context = {'project': project,
               'donations_flag': donations_flag,
               'user_rate': user_rating,
               'pics': project_pics,
               'donations': project_donation,
               'comments': comments,
               'report_form': Report(),
               'donation_form': Donate(),
               'related_projects': projects[:5]
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
        Project_rating.objects.update_or_create(
            project_id=id, user_id=user, defaults={'rating': rate})
        project_rating = project.project_rating_set.all().aggregate(Avg("rating"))[
            "rating__avg"]
        Projects.objects.update_or_create(
            id=id, defaults={'rating': project_rating})
        return redirect('project_page', id=id)


def search(request):
    if request.GET.get("search"):
        project_pics2 = {}

        res = []
        search_keyword = request.GET.get("search")
        search_tag_counter = Tags.objects.filter(
            Q(name__icontains=search_keyword)).count()
        if search_tag_counter:
            search_set = Project_tags.objects.filter(tag__name__icontains=search_keyword)

            for project in search_set:
                res.append(Projects.objects.get(id=project.project_id))

        elif search_tag_counter == 0:
            res = Projects.objects.filter(Q(title__icontains=search_keyword))

        else:
            res = ["No res"]

        for p in res:
            project_pics = Project_pics.objects.filter(project=p.id)
            project_pics2[p.id] = project_pics[0]
        context = {
            "projects_search": res,
            'pics': project_pics2,
        }
        return render(request, 'home_page.html', context)
    else:
        return render(request, 'home_page.html', {"NOdata": " your search key word doesn't match any projects !"})


def showCategoryProjects(request, cat_id):
    c = get_object_or_404(Categories, pk=cat_id)
    category_projects = c.projects_set.all()
    project_pics2 = {}

    print("category_projects", category_projects)

    for p in category_projects:
        print("P::", p)
        project_pics = Project_pics.objects.filter(project=p.id)
        project_pics2[p.id] = project_pics[0]
    context = {
        'category_name': c.title,
        'c': c,
        'category_projects': category_projects,
        'pics':  project_pics2
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
            messages.success(request,project_form.errors) 
    else:
        project_form = NewProject()
    # return render(request, reverse("users:projects"), {'project_form': project_form, })
    return redirect(reverse("users:projects"))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def donate(request, project_id):
    if request.method == 'POST':
        donate_form = Donate(request.POST)
        if donate_form.is_valid():
            new_donation = donate_form.save(commit=False)
            new_donation.user = request.user
            new_donation.project = Projects.objects.get(id=project_id)
            new_donation.save()
    
    return redirect(reverse("projects:project_page", args=[project_id]) )


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
            messages.error(request, 'Please login first!!!',
                           extra_tags='comment')
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
                new_report.project = Projects.objects.get(
                    pk=request.POST['project'])
            else:
                new_report.Comment = Project_comments.objects.get(
                    pk=request.POST['comment'])
            new_report.save()
            return HttpResponseRedirect(reverse("projects:project_page", args=[project_id]))
        else:
            print(report_form.errors)
    else:
        report_form = Report()
    context['report_form'] = report_form
    context['donation_form'] = Donate()

    return render(request, reverse("projects:project_page", args=[project_id]) , context)