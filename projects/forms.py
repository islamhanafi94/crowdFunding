# from django.forms import ModelForm
from django import forms
from django.forms import Select

from .models import Projects, Project_pics, Reports


class NewProject(forms.ModelForm):
    title = forms.CharField(max_length=50)
    details = forms.CharField(max_length=100)
    # category = forms.ModelChoiceField(
    #     queryset=Categories.objects.all(),
    #     widget=Select(attrs={'class': 'categories'}),
    # )
    total_target = forms.IntegerField()
    end_date = forms.DateField()

    class Meta:
        model = Projects
        fields = ('title', 'details', 'category',
                  'total_target', 'end_date')


class Report(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ('report',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Project_pics
        fields = ('image',)
