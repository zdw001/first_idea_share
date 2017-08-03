from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django import forms
from django.dispatch import receiver

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

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# photo = models.FileField(verbose_name=("Profile Picture"),
 #                      upload_to=upload_to("main.UserProfile.photo", "profiles"),
 #                      format="Image", max_length=255, null=True, blank=True)
	website = models.URLField(default='', blank=True)
	bio = models.TextField(max_length=500, default='', blank=True)
	phone = models.CharField(max_length=20, blank=True, default='')
	city = models.CharField(max_length=100, default='', blank=True)
	country = models.CharField(max_length=100, default='', blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created: 
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()




