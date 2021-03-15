# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.forms import SignUpForm, FriendshipRequestForm, FriendshipUpdateForm
from django.views import generic
from django.contrib.auth.models import User
from .models import Profile, Friendship
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from profiles.utils.mixins import UserIsRequesteeMixin
import pdb


def signup(request):
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


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('profiles:login'))
    # Redirect to a success page.

class FriendshipIndexView(LoginRequiredMixin, generic.ListView ):
    template_name = 'friendships/index.html'
    context_object_name = 'accepted-friendlist'
    form_class = FriendshipUpdateForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(FriendshipIndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = self.form_class

        return context

    def get_queryset(self):
        """Return the last ten posts."""
        # pub_date__lte means less than or equal to, today
        user = self.request.user

        crit1 = Q(pub_date__lte=timezone.now())
        crit2 = Q(author=user)
        crit3 = Q(author__in=friend_list)
        current_posts = Post.objects.filter( crit1 & (crit2 | crit3)).order_by('-pub_date')[:10]

        print("Friendship list", friend_list)
        print("Current Posts", current_posts)
        # self.request.user.
        # current_posts.annotate(is_liked_by_user=check_existing_dictionary_in_list('reactions', "user", self.request.user))
        for post in current_posts:
            post.is_liked_by_user = check_existing_dictionary_in_list(post.reactions.all(), "user", user)

        return current_posts


@login_required
def request_friendship(request, requestee_id):
    requestee = get_object_or_404(User, pk=requestee_id)
    if request.method == 'POST':
        form = FriendshipRequestForm(request.POST)
        if form.is_valid():
            friend_request = form.save(commit=False)
            friend_request.requester = request.user
            friend_request.requestee = requestee
            friend_request.save()

            messages.success(request, "Friend request has been sent.")
            return redirect('posts:index')
    else:
        return HttpResponseNotFound("404 Route not found.")


class FriendshipUpdateView(LoginRequiredMixin, UserIsRequesteeMixin, generic.UpdateView):
    model = Friendship
    form_class = FriendshipUpdateForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("profiles:detail", kwargs={"pk": self.request.user.id})


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    form_class = FriendshipUpdateForm

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        profile_belongs_to_user = self.request.user.id == self.kwargs["pk"]
        context['form'] = self.form_class if profile_belongs_to_user else None
        context['is_user_profile'] = profile_belongs_to_user
        # pdb.set_trace()
        if context['is_user_profile']:
            pending_friend_requests = Friendship.objects.filter(requester=self.request.user, status="Pending")
            context['pending_friend_requests'] = pending_friend_requests
            print("Pending Friend Requests ", pending_friend_requests)
        return context

    def get_queryset(self):
        """
            TODO Determine criteria for filtering
            """
        return Profile.objects
