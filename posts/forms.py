from django import forms
from .models import Post

class PostsForm(forms.Form):
    post_body = forms.CharField(label='Body', widget=forms.Textarea)
    post_title = forms.CharField(label='Body', max_length=100)
    pub_date = forms.DateField(label='Publish Date', widget=forms.SelectDateWidget())

    class Meta:
            model = Post
            fields = ('post_body', 'post_title', 'pub_date' )
