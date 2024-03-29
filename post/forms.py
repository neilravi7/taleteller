from django import forms
from django.forms import Select, TextInput
from post.models import Profile, Category, Article, Comment


class CategoryForm(forms.ModelForm):
    error_css_class = 'invalid-feedback'

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Updating attribute
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class ArticleForm(forms.ModelForm):
    error_css_class = 'invalid-feedback'

    # class meta options
    class Meta:
        # Article status constants
        DRAFTED = "DRAFTED"
        PUBLISHED = "PUBLISHED"
        # CHOICES
        STATUS_CHOICES = (
            (DRAFTED, 'Draft'),
            (PUBLISHED, 'Publish'),
        )
        
        model = Article
        fields = ["category", "title",
                "image_credit", "body", "tags", "status", "image", "deleted"]
        # update widgets
        widgets = {
            'status': Select(
                choices=STATUS_CHOICES,
                attrs={
                    "class": "form-control selectpicker",
                    "data-live-search": "true",
                    "title": "Select Status"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        updating forms attributes
        for field in self.fields:
            new_data = {
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

        # updating single attributes
        self.fields['deleted'].widget.attrs.update({'class': 'btn-check'})

class ArticleSearchForm(forms.Form):
    search = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update(
            {
                'class':'form-control', 
                'placeholder':'Enter search term..',
                'aria-label':"Enter search term...",
                'aria-describedby':"button-search",
            }
        )


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']
        widgets = {
            # 'article': forms.HiddenInput(),
            'comment':forms.Textarea(attrs={'rows':2, 'cols':4})
        }
    
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        for field in self.fields:
            new_data = {
                "class": 'form-control mb-3',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['comment'].widget.attrs.update(
            {
                "placeholder" :'Type your massage here'
            }
        )
        self.fields['name'].widget.attrs.update(
            {
                "placeholder" :'Name'
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                "placeholder" :'Email'
            }
        )