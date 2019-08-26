from django.urls import path
from . import views

# for updating/creating a Endorsement
urlpatterns = [
    path('bookmark', views.bookmark, name='bookmarks'),
]