from django.contrib import admin
from .models import Section, Topic


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