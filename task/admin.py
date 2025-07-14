from django.contrib import admin
from .models import Task
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Task)
class TaskAdmin(SummernoteModelAdmin):
    # Rich text editor for content field
    summernote_fields = ('content',)
    
    # Fields to display in the list view
    list_display = ('title', 'user', 'product', 'status', 'created_on', 'finished_on')
    
    # Filters in the right sidebar
    list_filter = ('status', 'user', 'product', 'created_on', 'finished_on')
    
    # Search capabilities
    search_fields = ('title', 'content', 'user__username', 'product__name')
    
    # Date-based navigation
    date_hierarchy = 'created_on'
    
    # Fields that cannot be edited
    readonly_fields = ('created_on',)
    
    # Custom ordering
    ordering = ('-created_on',)
    
    # Organize edit form
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'url', 'content')
        }),
        ('Relationships', {
            'fields': ('user', 'product')
        }),
        ('Status', {
            'fields': ('status', 'created_on', 'finished_on')
        }),
    )
