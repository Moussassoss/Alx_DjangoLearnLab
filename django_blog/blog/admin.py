# blog/admin.py
from django.contrib import admin
from .models import Post, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('published_date', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('post__title', 'author__username', 'content')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
