from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('get_all', views.get_all, name="get_all"),
    path('pic_search', views.pic_search, name="pic_search"),
    path('advance_search', views.advance_search, name="advance_search"),
    path('lostone', views.lostone, name="lostone"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
]