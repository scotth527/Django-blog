from django.contrib.auth.mixins import UserPassesTestMixin

class UserIsRequesteeMixin(UserPassesTestMixin):
    """Checks if the user of this function is the requestee. Only the requestee can respond to friendship request."""
    def test_func(self):
        obj = self.get_object()
        return obj.requestee == self.request.user

class UserIsRequesteeOrRequesterMixin(UserPassesTestMixin):
    """Checks if the user of this function is the requestee. Only the requestee can respond to friendship request."""
    def test_func(self):
        obj = self.get_object()
        return obj.requestee == self.request.user or obj.requester == self.request.user