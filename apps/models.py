from django.db import models


class LostOne(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=False, blank=False, max_length=100)
    email_address = models.CharField(null=False, blank=False, max_length=100)
    contact_number = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=False, blank=False, max_length=100)
    person_pic1 = models.ImageField(upload_to = 'collection/', default = 'collection/None/no-img.jpg')
    person_pic2 = models.ImageField(upload_to = 'collection/', default = 'collection/None/no-img.jpg')
    person_pic3 = models.ImageField(upload_to = 'collection/', default = 'collection/None/no-img.jpg')


class Contact(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    contact_number1 = models.CharField(null=True, blank=True, max_length=100)
    contact_number2 = models.CharField(null=True, blank=True, max_length=100)
    address = models.TextField(null=True, blank=True, max_length=300)
    note = models.TextField(null=True, blank=True)
    rescued = models.BooleanField(null=True, blank=True)
    died = models.BooleanField(null=True, blank=True)

