from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from post.models.author_models import Profile

class UserRegisterForm(UserCreationForm):
    error_css_class = 'invalid-feedback'
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Updating forms attributes
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class UserLoginForm(AuthenticationForm):
    
    error_css_class = 'invalid-feedback'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Updating forms attributes
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class ProfileForm(forms.ModelForm):
    error_css_class = 'invalid-feedback'
    first_name = forms.CharField(max_length=30) # label=_(u'Prénom'), 
    last_name = forms.CharField(max_length=30) # label=_(u'Nom')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

#        updating forms attributes
        for field in self.fields:
            new_data = {
                "class": 'form-control',
                "placeholder":field,
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
    
    def save(self, *args, **kwargs):
        super(ProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['user', 'email_confirmed', 'image']