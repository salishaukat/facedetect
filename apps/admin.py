from django.contrib import admin

from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['role','user']

admin.site.register(UserProfile, UserProfileAdmin)

# Register your models here.
class LostOneAdmin(admin.ModelAdmin):
      list_display = ['id','first_name','last_name','email_address','contact_number','age','status']

admin.site.register(LostOne, LostOneAdmin)

class SponsorAdmin(admin.ModelAdmin):
	list_display = ['id','name','email_address','contact_number','active']

admin.site.register(Sponsor, SponsorAdmin)

class ContactAdmin(admin.ModelAdmin):
	list_display = ['id','name','address','contact_number1','lost_one']

admin.site.register(Contact, ContactAdmin)

class ShelterAdmin(admin.ModelAdmin):
	list_display = ['id', 'shelter','address','contact_number1','lost_one']

admin.site.register(Shelter, ShelterAdmin)

class ShelterHomeAdmin(admin.ModelAdmin):
	list_display = ['id', 'name','address','area','contact_number1','contact_number2']

admin.site.register(ShelterHome, ShelterHomeAdmin)


class NewAdmin(admin.ModelAdmin):
    list_display = ['id','name','short_description']


admin.site.register(New, NewAdmin)
