from django.forms import ModelForm
from django import forms
from thinc.models import Idea
from django.utils import html

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


# create SubmitButtonField
class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="submit" name="%s" value="%s">' % (html.escape(name), html.escape(value))


class SubmitButtonField(forms.Field):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs["widget"] = SubmitButtonWidget

        super(SubmitButtonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value
		
class VoteForm(forms.Form):
    pass
