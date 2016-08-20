from django.contrib import admin
from .models import Section, Topic, Post, Profile


class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'created', 'status')
    list_filter = ('status', 'created')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ['title', 'created']

admin.site.register(Section, SectionAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug', 'created', 'status')
    list_filter = ('status', 'created')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ['title', 'created']

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('owner', 'topic', 'created', 'status')
    list_filter = ('status', 'created')
    search_fields = ('content',)
    date_hierarchy = 'created'
    ordering = ['owner', 'created']

admin.site.register(Post, PostAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo')

admin.site.register(Profile, ProfileAdmin)