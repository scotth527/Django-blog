# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.forms import SignUpForm, FriendshipRequestForm
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
            messages.error(request,'Username or password not correct.')
            return redirect('profiles:login')

    else:
        return render(request, 'profiles/signin.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('profiles:login'))
    # Redirect to a success page.

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


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    # login_url = '/profiles/login'
    # redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context.is_user_profile = self.request.user.id == kwargs['pk']
        if context.is_user_profile:
            pending_friend_requests = Friendship.objects.filter(requestor = self.request.user, status = "Pending")
            context.pending_friend_requests = pending_friend_requests
        return context

    def get_queryset(self):
            """
            TODO Determine criteria for filtering
            """
            return Profile.objects