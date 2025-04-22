from django.contrib import admin
from ProjectTodo.models import Task
class Taskadmin(admin.ModelAdmin):
    list_display=('title','due_date','is_completed','user')

admin.site.register(Task,Taskadmin)
# Register your models here.
