from django import forms
from .models import Post

class PostsForm(forms.ModelForm):
    post_body = forms.CharField(label='Body', widget=forms.Textarea, required=True)
    post_title = forms.CharField(label='Title', max_length=100, required=True)
    pub_date = forms.DateField(label='Publish Date', widget=forms.SelectDateWidget())

    class Meta:
            model = Post
            fields = ('post_body', 'post_title', 'pub_date' )
