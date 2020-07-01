from django import forms
from .models import Blog


class Blog_form(forms.Form):
    name = forms.CharField(label="Blog name", max_length=100, error_messages ={'required':"please enter title"})
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 20}),error_messages={'required':"please enter content"})
    tags = forms.ChoiceField(choices = Blog.TAGS)
    photo = forms.ImageField()

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if len(name) < 3:
             self.add_error("name", "my first custom error")

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name','photo','text', 'tags']

