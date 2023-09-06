from django.contrib import admin

# Register your models here.
from .models import TodoModel

admin.site.register(TodoModel)