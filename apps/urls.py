from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('lostone', views.lostone, name="lostone"),
    path('contact', views.contact, name="contact"),
]