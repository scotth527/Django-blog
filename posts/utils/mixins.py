from django.contrib.auth.mixins import UserPassesTestMixin

class UserIsAuthorMixin(UserPassesTestMixin):
    """Checks if the user of this function is the author. Only the author can edit, delete for example."""
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
