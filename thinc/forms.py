from django.forms import ModelForm
from django import forms
from thinc.models import (
    Idea,
    Profile,
    )
from django.utils import html
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class IdeaForm(ModelForm):
	class Meta:
		model = Idea
		# don't include votes because it is not editable
		fields = ('name', 'overview', 'description',)

class ContactForm(forms.Form):
    contact_name = forms.CharField()
    contact_email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:" 
        self.fields['contact_email'].label = "Your email:" 
        self.fields['content'].label = "What do you want to say?"

# registration form
class RegistrationForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('website', 'bio', 'phone', 'city', 'country')


