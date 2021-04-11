from django import forms
from .models import Post, Reaction, Comment

class PostsForm(forms.ModelForm):
    post_title = forms.CharField(label='Title', max_length=100, required=True)
    post_body = forms.CharField(label='Body', widget=forms.Textarea, required=True)
    pub_date = forms.DateField(label='Publish Date', widget=forms.SelectDateWidget())

    class Meta:
            model = Post
            fields = ('post_title', 'post_body',  'pub_date')

    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })


class CommentsForm(forms.ModelForm):
    comment_body = forms.CharField(label='Comment', max_length=120, required=True)

    class Meta:
                model = Comment
                fields = ('comment_body',)

    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

class ReactionsForm(forms.ModelForm):
    # reaction = forms.CharField(label='Reaction', max_length=100)

    class Meta:
                model = Reaction
                fields = ('reaction',)

    def __init__(self, *args, **kwargs):
        super(ReactionsForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

class PostUpdateForm(forms.ModelForm):
    post_title = forms.CharField(label='Title', max_length=100, required=True)
    post_body = forms.CharField(label='Body', widget=forms.Textarea, required=True)

    class Meta:
                model = Post
                fields = ('post_title', 'post_body')

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })