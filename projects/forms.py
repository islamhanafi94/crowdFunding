# from django.forms import ModelForm
import datetime
from django import forms
from django.forms import Select
from .models import Projects, Project_pics, Reports, Project_donations


class date_input(forms.DateInput):
    input_type = "date"

class NewProject(forms.ModelForm):
    title = forms.CharField(max_length=50)
    details = forms.CharField(max_length=100)
    total_target = forms.IntegerField(min_value=100)
    end_date = forms.DateField(widget=date_input())
    def clean_date(self):
        date = self.cleaned_data['end_date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date
    class Meta:
        model = Projects
        fields = ('title', 'details', 'category',
                  'total_target', 'end_date')


class Report(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ('report',)


class Donate(forms.ModelForm):
    donation = forms.IntegerField(min_value=1)
    class Meta:
        model = Project_donations
        fields = ('donation',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Project_pics
        fields = ('image',)
