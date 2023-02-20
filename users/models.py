from django.contrib.auth.models import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Proxy model, for storing additional information about the user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class TestUser:
    USERNAME = 'test'
    EMAIL = 'test@test.com'
    PASSWORD = 'Fw6isiVOSAdCbs1a0XTXokDV'

    def __new__(cls):
        return cls.get()

    @classmethod
    def get(cls) -> User:
        user, _ = User.objects.get_or_create(username=cls.USERNAME, email=cls.EMAIL, password=cls.PASSWORD)
        return user
