from django.contrib import admin
from django.contrib.auth.models import User
from .models import City, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

# Rejestracja modelu City w panelu administracyjnym
admin.site.register(City)
admin.site.unregister(User)  # Usunięcie domyślnego użytkownika
admin.site.register(User, UserAdmin)  # Zarejestrowanie nowego użytkownika z inline
