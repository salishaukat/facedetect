from django.contrib import admin


from .models import UserProfile, LostOne, Contact, Sponsor

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
