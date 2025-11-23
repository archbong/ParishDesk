from django.contrib import admin
from .models import Church, ChurchRole, UserProfile

# Register your models here.
@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "district", "phone", "email", "current_timezone", "created_by", "created_at", "updated_at")
    search_fields = ("name", "district", "phone", "email")

@admin.register(ChurchRole)
class ChurchRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "church", "role", "is_active")
    list_filter = ("role", "is_active")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone")
    search_fields = ("full_name", "user__username", "phone")
