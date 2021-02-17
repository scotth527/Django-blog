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
from posts.forms import PostsForm
from django.contrib import messages



class IndexView(LoginRequiredMixin, generic.ListView ):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'
    form_class = PostsForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['form'] = PostsForm

        return context

    def get_queryset(self):
        """Return the last five posts."""
        # pub_date__lte means less than or equal to, today
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'
    # login_url = '/profiles/login'
    # redirect_field_name = 'redirect_to'

    def get_queryset(self):
            """
            Excludes any questions that aren't published yet.
            """
            return Post.objects.filter(pub_date__lte=timezone.now())

@login_required
def create_post(request):
    # if this is a POST request we need to process the form data
    user = get_object_or_404(User, pk=request.user.id)
    print(request.POST)
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

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostsForm()

    return render(request, 'posts/index.html', {'form': form})
