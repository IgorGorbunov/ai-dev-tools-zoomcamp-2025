from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'completed', 'created_at')
    list_filter = ('completed',)
    search_fields = ('title', 'description')
