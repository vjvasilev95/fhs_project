from django import forms
from django.contrib.auth.models import User
from models import UserProfile, Page, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'shared')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    summary = forms.CharField()
    category = forms.CharField()


    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        exclude = ('category', 'flesch_score', 'sentiment_score', 'subjectivity_score')


    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class PasswordReset(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordReset, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        if self.clean_data.get('oldpassword') and not self.user.check_password(self.clean_data['oldpassword']):
            raise ValidationError('Please type your current password.')
        return self.clean_data['oldpassword']

    def clean_password2(self):
        if self.clean_data.get('password1') and self.clean_data.get('password2') and self.clean_data['password1'] != self.clean_data['password2']:
            raise ValidationError('The new passwords are not the same')
        return self.clean_data['password2']