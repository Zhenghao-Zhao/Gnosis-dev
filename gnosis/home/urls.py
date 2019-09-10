from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_recent_10_authors/', views.get_recent_10_authors, name='recent_10_authors'),
]
