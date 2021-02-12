from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Post, Comment
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin,generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'
    login_url = '/profiles/login'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        """Return the last five posts."""
        # pub_date__lte means less than or equal to, today
        print("Testing authentication", self.request.user.is_authenticated)

        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'
    login_url = '/profiles/login'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            return Post.objects.filter(pub_date__lte=timezone.now())