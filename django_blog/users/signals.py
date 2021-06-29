from django.db.models.signals import post_save
from django.contrib.auth.models import User  
from django.dispatch import receiver
from users.models import Profile


# the receiver is the create_profile func
# create a user profile for each new user created
# signal=post_save
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# save profile everytime user object gets saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
