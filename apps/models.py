from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.template.defaultfilters import truncatechars

upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='uploads')

class UserProfile(models.Model):
  user = models.OneToOneField(User, related_name="profile", on_delete=True)
  CHOICES = (
        ('reporter', 'reporter'),
        ('rescuer', 'rescuer'),
    )
  role = models.CharField(
        max_length=200,
        choices=CHOICES,
        default=1
    )

class LostOne(models.Model):
    #uid = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    email_address = models.CharField(null=True, blank=True, max_length=100)
    contact_number = models.CharField(null=True, blank=True, max_length=100)
    age = models.IntegerField(null=True, blank=True)
    status = models.CharField(null=False, blank=False, max_length=100)
    area = models.CharField(null=True, blank=True, max_length=900)
    country = models.CharField(null=False, blank=False, max_length=100)
    person_pic1 = models.CharField(null=True, blank=True, max_length=1000)
    person_pic2 = models.CharField(null=True, blank=True, max_length=1000)
    person_pic3 = models.CharField(null=True, blank=True, max_length=1000)
    gender = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField(null=True, blank=True, max_length=100)
    folder_name = models.CharField(null=True, blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)


class ShelterHome(models.Model):
    AREA_CHOICES = (
    ("AB - Bahama Coral Island", "AB - Bahama Coral Island"),
    ("AB - Bahama Palm Shores", "AB - Bahama Palm Shores"),
    ("AB - Blackwood Village", "AB - Blackwood Village"),
    ("AB - Central Pines", "AB - Central Pines"),
    ("AB - Cooper's Town", "AB - Cooper's Town"),
    ("AB - Crossing Rocks", "AB - Crossing Rocks"),
    ("AB - Dundas Town", "AB - Dundas Town"),
    ("North Andros", "North Andros"),
    ("Great Inagua", "Great Inagua"),
    ("South Andros", "South Andros"),
    ("Great Abac", "Great Abaco"),
    ("Grand Bahama", "Grand Bahama"),
    ("Long Island, Bahamas", "Long Island, Bahamas"),
    ("Acklins", "Acklins"),
    ("Eleuthera", "Eleuthera"),
    ("Cat Island", "Cat Island"),
    ("Mayaguana", "Mayaguana"),
    ("Crooked Island, Bahamas", "Crooked Island, Bahamas"),
    ("New Providence", "New Providence"),
    ("Exuma", "Exuma"),
    ("San Salvador Island", "San Salvador Island"),
    ("Little Inagua", "Little Inagua"),
    ("Rum Cay", "Rum Cay"),
    ("Little Abaco", "Little Abaco"),
    ("Samana Cay", "Samana Cay"),
    ("Ragged Island", "Ragged Island"),
    ("Berry Islands", "Berry Islands"),
    ("Bimini", "Bimini"),
    )    
    name = models.CharField(null=False, blank=False, max_length=100)
    contact_number1 = models.CharField(null=True, blank=True, max_length=100)
    contact_number2 = models.CharField(null=True, blank=True, max_length=100)
    address = models.TextField(null=True, blank=True, max_length=300)
    area = models.CharField(null=True, blank=True, max_length=200, choices=AREA_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    

class Contact(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    contact_number1 = models.CharField(null=True, blank=True, max_length=100)
    contact_number2 = models.CharField(null=True, blank=True, max_length=100)
    address = models.TextField(null=True, blank=True, max_length=300)
    area = models.CharField(null=True, blank=True, max_length=100)
    note = models.TextField(null=True, blank=True, max_length=500)
    area = models.CharField(null=True, blank=True, max_length=100)
    lost_one = models.ForeignKey(LostOne, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

class Shelter(models.Model):
    #shelter_id = models.IntegerField(null=True, blank=True)
    shelter = models.CharField(null=False, blank=False, max_length=100)
    contact_number1 = models.CharField(null=True, blank=True, max_length=100)
    contact_number2 = models.CharField(null=True, blank=True, max_length=100)
    address = models.TextField(null=True, blank=True, max_length=300)
    area = models.CharField(null=True, blank=True, max_length=100)
    note = models.TextField(null=True, blank=True, max_length=500)
    status = models.CharField(null=True, blank=True, max_length=100)
    area = models.CharField(null=True, blank=True, max_length=100)
    lost_one = models.ForeignKey(LostOne, on_delete=models.CASCADE, null=True)
    person_pic4 = models.CharField(null=True, blank=True, max_length=1000)
    person_pic5 = models.CharField(null=True, blank=True, max_length=1000)
    person_pic6 = models.CharField(null=True, blank=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

class Sponsor(models.Model):
    #sid = models.IntegerField(null=True, blank=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    company_name = models.CharField(null=False, blank=False, max_length=100)
    email_address = models.CharField(null=False, blank=False, max_length=100)
    contact_number = models.CharField(null=True, blank=True, max_length=100)
    company_logo = models.CharField(null=False, blank=False, max_length=100)
    active = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)


class New(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    details = RichTextField(config_name='awesome_ckeditor',null=True, blank=True)
    image1 = models.FileField(upload_to='images', storage=upload_storage, null=True, blank=True)
    video = models.FileField(upload_to='videos', storage=upload_storage, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    @property
    def short_description(self):
        from django.utils.html import strip_tags
        return truncatechars(strip_tags(self.details), 70)