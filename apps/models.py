from django.db import models
from django.contrib.auth.models import User

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
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=False, blank=False, max_length=100)
    email_address = models.CharField(null=False, blank=False, max_length=100)
    contact_number = models.CharField(null=True, blank=True, max_length=100)
    age = models.IntegerField(null=False, blank=False)
    status = models.CharField(null=False, blank=False, max_length=100)
    area = models.CharField(null=True, blank=True, max_length=900)
    country = models.CharField(null=False, blank=False, max_length=100)
    person_pic1 = models.CharField(null=False, blank=False, max_length=100)
    person_pic2 = models.CharField(null=True, blank=True, max_length=100)
    person_pic3 = models.CharField(null=True, blank=True, max_length=100)
    gender = models.CharField(null=False, blank=False, max_length=100)
    name = models.CharField(null=True, blank=True, max_length=100)
    folder_name = models.CharField(null=True, blank=True, max_length=100)


class Contact(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    contact_number1 = models.CharField(null=True, blank=True, max_length=100)
    contact_number2 = models.CharField(null=True, blank=True, max_length=100)
    address = models.TextField(null=True, blank=True, max_length=300)
    area = models.CharField(null=True, blank=True, max_length=100)
    note = models.TextField(null=True, blank=True)
    rescued = models.BooleanField(null=True, blank=True, default=False)
    died = models.BooleanField(null=True, blank=True, default=False)
    area = models.CharField(null=False, blank=False, max_length=100)
    lost_one = models.ForeignKey(LostOne, on_delete=models.CASCADE, null=True)


class Sponsor(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    company_name = models.CharField(null=False, blank=False, max_length=100)
    email_address = models.CharField(null=False, blank=False, max_length=100)
    contact_number = models.CharField(null=True, blank=True, max_length=100)
    company_logo = models.CharField(null=False, blank=False, max_length=100)

class Comments(models.Model):
    lost_one = models.ForeignKey(LostOne, on_delete=models.CASCADE, null=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    comment = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    
