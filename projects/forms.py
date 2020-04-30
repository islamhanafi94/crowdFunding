# from django.forms import ModelForm
from django import forms
from django.forms import Select

from .models import Projects, Project_pics, Reports, Project_donations


class date_input(forms.DateInput):
    input_type = "date"

class NewProject(forms.ModelForm):
    title = forms.CharField(max_length=50)
    details = forms.CharField(max_length=100)
    total_target = forms.IntegerField()
    end_date = forms.DateField(widget=date_input())

    class Meta:
        model = Projects
        fields = ('title', 'details', 'category',
                  'total_target', 'end_date')


class Report(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ('report',)


class Donate(forms.ModelForm):
    class Meta:
        model = Project_donations
        fields = ('donation',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Project_pics
        fields = ('image',)
