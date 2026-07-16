from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )