from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    # CASCADE: if user is deleted, delete the profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1:1 relationship with User model
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # upload image to dir: 'profile_pics'

    def __str__(self):
        return f'{self.user.username} Profile'


