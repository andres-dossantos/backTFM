from django.contrib import admin
from .models import Form

# Register your models here.

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("user", "work", "salary", "age", "gender", "country", "weather", "created_at", "updated_at")
    list_filter = ("user", "work", "salary", "age", "gender", "country", "weather", "created_at", "updated_at")
