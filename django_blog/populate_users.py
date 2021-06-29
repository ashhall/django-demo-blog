import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
	'django_blog.settings')

import django
django.setup()

from faker import Faker 
from django.contrib.auth.models import User
from users.models import Profile

faker_obj = Faker()
profiles = []

def add_fake_profile():
	fake = faker_obj.profile()
	# get_or_create returns a tuple (object, created)
	fake_user = User.objects.get_or_create(
		username=fake['username'],
		email=fake['mail'],
		password=os.environ.get('DJANGO_TEST_PASS')
	)[0]
	fake_profile = Profile.objects.get_or_create(user=fake_user)[0]
	fake_profile.save()


def populate_user_profiles(n=5):

	for profile in range(n):
		add_fake_profile()


if __name__ == '__main__':
	print('generating fake profiles...')
	populate_user_profiles()
	print('finished')