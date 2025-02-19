from django.contrib import admin
from .models import Form

# Register your models here.

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "created_at", "updated_at")
    list_filter = ("user", "created_at", "updated_at")
