from django.contrib.auth.mixins import UserPassesTestMixin

class UserIsAuthorMixin(UserPassesTestMixin):
    """Checks if the user of this function is the author. Only the author can edit, delete for example."""
    def test_func(self):
        obj = self.get_object()
        print("User is author mixin", obj.author, self.request.user, obj.author == self.request.user )
        return obj.author == self.request.user

