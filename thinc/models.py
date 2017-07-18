from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Idea(models.Model):
	user = models.ForeignKey('auth.User')
	name = models.CharField(max_length=255, default="", editable=True)
	overview = models.TextField()
	description = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True, null=True)
	updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
	votes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name 
