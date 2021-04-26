# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.forms import SignUpForm, FriendshipRequestForm, FriendshipUpdateForm
from django.views import generic
from django.contrib.auth.models import User
from .models import Profile, Friendship
from posts.models import Post
from posts.forms import CommentsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from profiles.utils.mixins import UserIsRequesteeMixin, UserIsRequesteeOrRequesterMixin
from profiles.utils.utils import get_friendlist, get_friend_suggestions, get_mutual_friends, check_friendship_status
from haystack.query import SearchQuerySet
import pdb

def signup(request):
    '''
    Function is to create new profiles and at the same time creates new users
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/posts/')
    else:
        form = SignUpForm()

    return render(request, 'profiles/signup.html', {'form': form})

def signin(request):
    '''
    Logs in the user and authenticates them
    :param request:
    :return:
    '''
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('posts:index')

        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Username or password not correct.')
            return redirect('profiles:login')

    else:
        return render(request, 'profiles/signin.html', {'form': form})



def logout_view(request):
    '''
    Logout the user function, redirects user to login page
    :param request:
    :return:
    '''
    logout(request)
    return HttpResponseRedirect(reverse('profiles:login'))
    # Redirect to a success page.


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    form_class = FriendshipUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        profile = self.get_object()
        user = self.request.user
        profile_belongs_to_user = user.id == self.kwargs["pk"]
        user_friendlist = get_friendlist(self.request.user)

        context['form'] = self.form_class if profile_belongs_to_user else None
        context['comment_form'] = CommentsForm
        context['is_user_profile'] = profile_belongs_to_user
        context['posts'] = Post.objects.filter(author=profile.user).order_by('-pub_date')[:10]
        context['friend_list'] = user_friendlist
        # pdb.set_trace()
        if context['is_user_profile']:
            pending_friend_requests = Friendship.objects.filter(requestee=self.request.user, status="Pending")
            context['pending_friend_requests'] = pending_friend_requests
        else:
            profile = self.get_object().user
            context['is_friend_of_user'] = profile in user_friendlist
            friendship_status = check_friendship_status(user, profile)
            print("Friendship status", vars(friendship_status))

        return context

    def get_queryset(self):
        return Profile.objects


class FriendshipIndexView(LoginRequiredMixin, generic.ListView):
    """
    Returns a list of friends that have been accepted
    """
    template_name = 'friendships/index.html'
    context_object_name = 'accepted_friendlist'
    form_class = FriendshipUpdateForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(FriendshipIndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = self.form_class

        return context

    def get_queryset(self):
        """Return the user's friendlist. """
        user = get_object_or_404(User,pk=self.kwargs["pk"])
        return get_friendlist(user)

class FriendshipSuggestionIndexView(LoginRequiredMixin, generic.ListView):
    """
    Returns a list of suggested friends, not already friends with
    """
    template_name = 'friendships/suggestions.html'
    context_object_name = 'suggested_friendlist'
    form_class = FriendshipRequestForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(FriendshipSuggestionIndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = self.form_class

        return context

    def get_queryset(self):
        """Return the user's friendlist. """
        user = self.request.user
        suggestion_count = self.kwargs["suggestion_count"]
        friend_suggestions = get_friend_suggestions(user, suggestion_count)
        for friend in friend_suggestions:
           friend.mutual_friends = get_mutual_friends(user, friend.user)
        return friend_suggestions

    # TODO: Complete this friendship suggestion function


@login_required
def request_friendship(request, requestee_id):
    '''
    Adds a new entry to the friendship table to establish a relationship between users
    :param request:
    :param requestee_id:
    :return:
    '''
    requestee = get_object_or_404(User, pk=requestee_id)
    if request.method == 'POST':
        form = FriendshipRequestForm(request.POST)
        if form.is_valid():
            friend_request = form.save(commit=False)
            friend_request.requester = request.user
            friend_request.requestee = requestee
            friend_request.save()

            messages.success(request, "Friend request has been sent.")
            return HttpResponseRedirect(reverse('posts:index'))
    else:
        return HttpResponseNotFound("404 Route not found.")


class FriendshipUpdateView(LoginRequiredMixin, UserIsRequesteeMixin, generic.UpdateView):
    model = Friendship
    form_class = FriendshipUpdateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("profiles:detail", kwargs={"pk": self.request.user.id})


class FriendshipDeleteView(LoginRequiredMixin, UserIsRequesteeOrRequesterMixin, generic.DeleteView):
    # specify the model you want to use
    model = Friendship
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse("profiles:friend-list", kwargs={"pk": self.request.user.id})

class SearchUserIndexView(LoginRequiredMixin, generic.ListView):
    """
    Returns a list of friends
    """
    template_name = 'profiles/search_result.html'
    context_object_name = 'search_result'
    form_class = FriendshipRequestForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(FriendshipIndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = self.form_class

        return context

    def get_queryset(self):
        """Return the user's friendlist."""
        search_value = self.kwargs["pk"]
        return get_friendlist(user)