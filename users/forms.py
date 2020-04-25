from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users
from django.contrib.auth import authenticate

class RegistraionForm(UserCreationForm):
    email = forms.EmailField(help_text="enter your email...")

    class Meta:
        model = Users
        fields = ('email','first_name','last_name','phone','photo','password1','password2')





class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('email','password')


    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('invalid login data...')






class UpdateUserForm(forms.ModelForm):

    YEARS= [x for x in range(1940,2021)]
    date_birth = forms.DateField(label="enter your birthdate",widget=forms.SelectDateWidget(years=YEARS),initial='1891-1-1')
    photo = forms.ImageField(required=False)
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','photo','date_birth','facebook_link','country')


    # def clean_first_name(self):
    #     if self.is_valid():
    #         first_name = self.cleaned_data['first_name'].strip()
    #         if first_name :
    #             return first_name
    #         else:
    #             raise forms.ValidationError('first name can\'t be empty')
            

    # def clean_last_name(self):
    #     if self.is_valid():
    #         last_name = self.cleaned_data['last_name'].strip()
    #         if last_name :
    #             return last_name
    #         else:
    #             raise forms.ValidationError('last name can\'t be empty')

    
    def clean_photo(self):
        if self.is_valid():
            photo = self.cleaned_data['photo']
            if photo:
                print("instance photo is :",self.instance.photo)
                print("photo is :",self.cleaned_data['photo'])
                return photo
            else:
                raise forms.ValidationError('please upload a valid photo')