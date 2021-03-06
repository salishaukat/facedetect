from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home/<str:contact>', views.index, name="index"),
    path('sponsor', views.sponsor, name="sponsor"),
    path('search', views.search, name="search"),
    path('search/<int:id>', views.search, name="search"),
    path('get_all', views.get_all, name="get_all"),
    path('pic_search', views.pic_search, name="pic_search"),
    path('live_search', views.live_search, name="live_search"),
    path('advance_search', views.advance_search, name="advance_search"),
    path('lostone', views.lostone, name="lostone"),
    path('lostone/<int:lost_one_id>', views.lostone, name="lostone"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('comment', views.comments, name="comment"),
    path('reports', views.reports, name="reports"),
    path('reports/<str:search>', views.reports, name="reports"),
    path('get_all_lost_one/<int:lost_one_id>',views.get_all_lost_one, name="get_all_lost_one"),
    path('live', views.live, name="live"),
    path('get_face', views.get_face_from_image, name="get_face"),
    path('news', views.news, name="news"),
    path('about-us', views.about_us, name="about-us"),
    path('news_details/<int:id>', views.news_details, name="news_details"),
    path('found/<int:id>', views.found, name="found")
]