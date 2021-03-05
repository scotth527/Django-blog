from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Post, Comment, Reaction
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin, DeleteView
from posts.forms import PostsForm, CommentsForm, ReactionsForm
from django.contrib import messages
from utils.dictionary_utils import check_existing_dictionary_in_list
import pdb
from django.db.models.expressions import Case, When, Value, Exists
from django.db.models import Count, Q

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
        current_posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # current_posts.annotate(is_liked_by_user=check_existing_dictionary_in_list('reactions', "user", self.request.user))
        for post in current_posts:
            post.is_liked_by_user = check_existing_dictionary_in_list(post.reactions.all(), "user", self.request.user)

        return current_posts

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(DetailView, self).get_context_data(**kwargs)
            # Create any data and add it to the context
            context['form'] = self.form_class
            post = context['post']
            comments = post.comment_set.all()
            post.is_liked_by_user = check_existing_dictionary_in_list(post.reactions.all(), "user", self.request.user)
            # comments.annotate(is_liked_by_user=Count('reactions', filter=Q(reactions__user=self.request.user)))
            comments.annotate(is_liked_by_user=Count('reactions'), filter=Q(reactions__user=self.request.user))

            # print("Commments", comments, comments[0].is_liked_by_user)
            # comments.annotate(is_liked_by_user=Count('reactions'))
            # for i, comment in enumerate(comments):
               # print("Comment is liked", comment.is_liked_by_user)
                 # comment.is_liked_by_user = check_existing_dictionary_in_list(comment.reactions.all(), "user", self.request.user)
              # print("Was comment liked by user?", comment.is_liked_by_user, comment.comment_body)
                # comment.is_liked_by_user = check_existing_dictionary_in_list(comment.reactions.all(), "user", self.request.user)
                # context['is_liked_by_user'] = check_existing_dictionary_in_list(post.reactions.all(), "user", self.request.user)
            # pdb.set_trace()
            return context

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            post = Post.objects.filter(pub_date__lte=timezone.now())
            user_reaction = Reaction.objects.filter(
                user=self.request.user,

            )
            # comments = post.comment_set.all()
            # comments.annotate(is_liked_by_user= Count('reactions', filter=Q(reactions__user=self.request.user)) )
            # print("POST VALUES", post.values('comment').annotate(is_liked_by_user=Exists(user_reaction)))

            # for item in post:
                # item.annotate(is_liked_by_user = False )
                # item.is_liked_by_user = check_existing_dictionary_in_list(item.reactions.all(), "user", self.request.user)


            try:
                pass
                # for comment in post[0].comment_set.all():
                    # print("COMMENT INFO", comment, comment.id)
                    # comment.is_liked_by_user = check_existing_dictionary_in_list(comment.reactions.all(), "user", self.request.user)
                    # print("Comment is liked status", comment.is_liked_by_user)
                # for comment in post[0].comment_set.all():
                   #  print("Comment is liked", comment, comment.is_liked_by_user)
            except Exception as e:
                 print("", e)

            # pdb.set_trace()
            return post

class PostsDeleteView(LoginRequiredMixin, generic.DeleteView):
    # specify the model you want to use
    model = Post

    # can specify success url
    # url to redirect after sucessfully
    # deleting object
    success_url = "/"

@login_required
def toggle_reaction(request, object_id, object_type):
    user = get_object_or_404(User, pk=request.user.id)
    object = None
    if object_type == "comment":
        object = get_object_or_404(Comment, pk=object_id)
    elif object_type == "post":
        object = get_object_or_404(Post, pk=object_id)

    user_reaction = object.reactions.filter(user=user)
    user_has_reacted_to_object = user_reaction.count() > 0

    if request.method == 'POST' and object:
        form = ReactionsForm(request.POST)
        # pdb.set_trace()
        if form.is_valid() and not user_has_reacted_to_object:
            reaction = form.save(commit=False)
            reaction.user = user
            reaction.object_id = object_id
            reaction.content_object = object
            reaction.save()

        else:
            user_reaction.delete()

        return redirect(request.META.get('HTTP_REFERER', 'posts:index'))
    else:
        print("Object was NONE")


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
