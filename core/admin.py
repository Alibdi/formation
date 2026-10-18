from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, User

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code')
    search_fields = ('nom', 'code')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'service', 'matricule', 'is_staff')
    list_filter = ('role', 'service', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Agent', {'fields': ('role', 'service', 'matricule')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Agent', {'fields': ('role', 'service', 'matricule')}),
    )
