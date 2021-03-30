import datetime
from haystack import indexes
from profiles.models import Profile
from django.contrib.auth.models import User

class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    # document = True, main item being searched
    # use_template , can make template of fields from the main search field
    text = indexes.EdgeNgramField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    address = indexes.CharField(model_attr='address')
    city = indexes.CharField(model_attr='city')
    state = indexes.CharField(model_attr='state')
    username = indexes.CharField()
    email = indexes.CharField()

    content_auto = indexes.EdgeNgramField(model_attr='first_name')

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        users = self.get_model().objects.filter().select_related('user')
        return users

    def prepare_username(self, obj):
        return obj.user.username

    def prepare_email(self, obj):
        return obj.user.email