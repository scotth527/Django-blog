from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Post, Comment
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from posts.forms import PostsForm, CommentsForm, ReactionsForm
from django.contrib import messages
from utils.dictionary_utils import check_existing_dictionary_in_list
import pdb


class IndexView(LoginRequiredMixin, generic.ListView ):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'
    form_class = PostsForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = PostsForm
        context['comment_form'] = CommentsForm

        return context

    def get_queryset(self):
        """Return the last five posts."""
        # pub_date__lte means less than or equal to, today
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(DetailView, self).get_context_data(**kwargs)
            # Create any data and add it to the context
            context['form'] = self.form_class


            return context

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            return Post.objects.filter(pub_date__lte=timezone.now())

@login_required
def toggle_reaction(request, object_id, object_type):
    user = get_object_or_404(User, pk=request.user.id)
    object = None
    if object_type == "comment":
        object = get_object_or_404(Comment, pk=object_id)
    elif object_type == "post":
        object = get_object_or_404(Post, pk=object_id)

    print("Object reaction set", object.reactions.all()) # Check if user already liked post/comment
    # found_user = [profile for profile in object.reaction_set if profile["username"] == request.user.username]
    # object.__dict__

    if request.method == 'POST' and object != None:
        form = ReactionsForm(request.POST)
        # pdb.set_trace()
        if form.is_valid():

            reaction = form.save(commit=False)
            reaction.user = user
            reaction.object_id = object_id
            reaction.content_object = object
            print("Reaction", reaction)
            reaction.save()
            # Search the post or comment
            # Check if the user has contributed to the comment
            # If the user has contributed then remove it
            # If the user hasn't, add a reaction
            # Save form
            return redirect('posts:index')
        else:
            print("Form Invalid", form.errors)
    else:
        pass


@login_required
def create_post(request):
    # if this is a POST request we need to process the form data
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = PostsForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Form submission successful')
            # redirect to a new URL:
            return redirect('posts:index')
        else:
            print("Form Invalid", request.POST)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostsForm()

    return render(request, 'posts/index.html', {'form': form})

@login_required
def create_comment(request, post_id):
    user = get_object_or_404(User, pk=request.user.id)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
            # create a form instance and populate it with data from the request:

            form = CommentsForm(request.POST)
            # check whether it's valid:

            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                print("Successfully saved.")
                messages.success(request, 'Comment submission successful')
                # redirect to a new URL:
                return redirect(reverse('posts:detail', args=(post.id,)))
            else:
                print("Form Invalid", request.POST)

    else:
        form = PostsForm()

        return render(request, 'posts/index.html', {'form': form})
    pass
