from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Post, Comment


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five posts."""
        # pub_date__lte means less than or equal to, today
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            return Post.objects.filter(pub_date__lte=timezone.now())