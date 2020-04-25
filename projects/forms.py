from django.forms import ModelForm
from .models import Projects


class NewProject(ModelForm):
    class Meta:
        model = Projects
        fields = ('title', 'details', 'category',
                  'total_target', 'end_date')
