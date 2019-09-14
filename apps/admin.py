from django.contrib import admin


from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['role','user']

admin.site.register(UserProfile, UserProfileAdmin)

# Register your models here.
