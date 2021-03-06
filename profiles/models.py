from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

FRIENDSHIP_STATUS_CHOICES = (
                  ("Pending", "Pending"),
                  ("Accept", "Accept"),
                  ("Decline", "Decline")
)

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, default="Miami")
    state = models.CharField(max_length=50, default="FL")
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    @receiver(post_save, sender=User)

    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
            return self.first_name + " " + self.last_name

class Friendship(models.Model):
      status = models.CharField(max_length=50, choices=FRIENDSHIP_STATUS_CHOICES, default="Pending")
      requester = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='requester')
      requestee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='requestee')

      class Meta:
        unique_together = ('requester', 'requestee')
