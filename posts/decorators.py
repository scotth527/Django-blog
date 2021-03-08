from django.core.exceptions import PermissionDenied
from .models import Post, Comment, Reaction
from django.shortcuts import render, get_object_or_404, redirect
import functools

def user_is_author(object_type="post"):
    """Checks if the user of this function is the author. Only the author can edit, delete for example."""
    def actual_decorator(function):
        @functools.wraps(function)
        def wrap(request, *args, **kwargs):
            entry = None
            if object_type == "post":
                entry = get_object_or_404(Post,pk=kwargs['pk'])
            elif object_type == "comment":
                entry = get_object_or_404(Comment, pk=kwargs['pk'])

            if entry.author == request.user:
                return function(request, *args, **kwargs)
            else:
                print("Request denied")
                raise PermissionDenied
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap

    return actual_decorator