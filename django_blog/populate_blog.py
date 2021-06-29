import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
	'django_blog.settings')

import django
django.setup()

import random
from faker import Faker 
from blog.models import Post
from django.contrib.auth.models import User

fake = Faker()
users = User.objects.all()

def add_fake_post():
	title = fake.sentence(nb_words=5).strip('.').title()
	content = fake.paragraph(nb_sentences=10)
	author = random.choice(users) 
	fake_post = Post.objects.get_or_create(title=title, content=content, author=author)[0]
	fake_post.save()


def populate_blog(n=20):
	for post in range(n):
		add_fake_post()


if __name__ == '__main__':
	print('generating fake posts...')
	populate_blog()
	print('finished')