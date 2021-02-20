from django import forms
from .models import Post, Reaction, Comment

class PostsForm(forms.ModelForm):
    post_title = forms.CharField(label='Title', max_length=100, required=True)
    post_body = forms.CharField(label='Body', widget=forms.Textarea, required=True)
    pub_date = forms.DateField(label='Publish Date', widget=forms.SelectDateWidget())

    class Meta:
            model = Post
            fields = ('post_title', 'post_body',  'pub_date' )

class CommentsForm(forms.ModelForm):
    comment_body = forms.CharField(label='Comment', max_length=120, required=True)

    class Meta:
                model = Comment
                fields = ('comment_body', )

class ReactionsForm(forms.ModelForm):
    pass
