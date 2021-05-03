from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Post, Comment, Reaction
from profiles.models import Friendship
from profiles.utils.utils import get_friendlist
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.utils.mixins import UserIsAuthorMixin
from django.views.generic.edit import ModelFormMixin, DeleteView, UpdateView
from posts.forms import PostsForm, CommentsForm, ReactionsForm, PostUpdateForm
from django.contrib import messages
from utils.dictionary_utils import check_existing_dictionary_in_list
import pdb
from django.db.models.expressions import Case, When, Value, Exists
from django.db.models import Count, Q
from .decorators import user_is_author

class PostsIndexView(LoginRequiredMixin, generic.ListView ):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'
    form_class = PostsForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PostsIndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = PostsForm
        context['comment_form'] = CommentsForm

        return context

    def get_queryset(self):
        """Return the last ten posts."""
        # pub_date__lte means less than or equal to, today
        user = self.request.user
        friend_list = get_friendlist(user)

        non_future_post = Q(pub_date__lte=timezone.now())
        post_belongs_to_user = Q(author=user)
        post_belongs_to_friend = Q(author__in=friend_list)
        current_posts = Post.objects.filter(non_future_post & (post_belongs_to_user | post_belongs_to_friend)).order_by('-pub_date')

        # TODO: Allow user to fetch more posts if desired

        for post in current_posts:
            post.is_liked_by_user = check_existing_dictionary_in_list(post.reactions.all(), "user", user)

        return current_posts

class PostsDetailView(LoginRequiredMixin,generic.DetailView):
    """"Returns the specified post, cannot show a post that has not been published yet."""
    model = Post
    template_name = 'posts/detail.html'
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(PostsDetailView, self).get_context_data(**kwargs)
            # Create any data and add it to the context
            context['form'] = self.form_class
            post = context['post']
            comments = post.comment_set.all()
            #Checks if the user has liked these comments, used for rendering a like vs unlike button
            context['comments'] = comments.annotate(is_liked_by_user=Count('reactions__reaction', filter=Q(reactions__user=self.request.user)))

            return context

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            post = Post.objects.filter(pub_date__lte=timezone.now())
            user_reaction = Reaction.objects.filter(
                user=self.request.user,
            )

            post = post.annotate(is_liked_by_user=Count('reactions__reaction', filter=Q(reactions__user=self.request.user)))
            return post


class PostsDeleteView(LoginRequiredMixin, UserIsAuthorMixin, generic.DeleteView):
    # specify the model you want to use
    model = Post
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url = "/"

class PostUpdateView(LoginRequiredMixin, UserIsAuthorMixin, generic.UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("posts:detail", kwargs={"pk": pk})

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

    if request.method == 'POST' and object and request.is_ajax:
        form = ReactionsForm(request.POST)
        # pdb.set_trace()
        if form.is_valid() and not user_has_reacted_to_object:
            reaction = form.save(commit=False)
            reaction.user = user
            reaction.object_id = object_id
            reaction.content_object = object
            reaction.save()

        elif user_has_reacted_to_object:
            user_reaction.delete()

        updated_count = object.reactions.count()
        print("Updated counts", updated_count)
        return JsonResponse({"object_reaction_count": updated_count}, status=200)
    else:
        print("Request.method", request.method, object)
        return JsonResponse({"error": ""}, status=400)


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
            post = form.save(commit=False)
            post.author = user
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
                comment = form.save(commit=False)
                comment.author = user
                comment.post = post
                comment.save()
                messages.success(request, 'Comment submission successful')
                # redirect to a new URL:
                return redirect(reverse('posts:detail', args=(post.id,)))
            else:
                print("Form Invalid", request.POST)

    else:
        form = PostsForm()

        return render(request, 'posts/index.html', {'form': form})

class CommentsDeleteView(LoginRequiredMixin, UserIsAuthorMixin, generic.DeleteView):
    # specify the model you want to use
    model = Comment
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url = "/"



    # TODO: functionality for this path
