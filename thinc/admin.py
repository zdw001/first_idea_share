from django.contrib import admin

# import models
from thinc.models import Idea

# set up automated slug creation
class IdeaAdmin(admin.ModelAdmin):
	model = Idea
	list_display = ('user', 'name', 'overview', 'description', 'published_date', 'votes',)
	prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Idea, IdeaAdmin)