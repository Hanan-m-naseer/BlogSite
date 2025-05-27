from django.contrib import admin
from .models import BlogPost, Profile

# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','profile_pic')