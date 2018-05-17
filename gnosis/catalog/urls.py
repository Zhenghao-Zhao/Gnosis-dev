from django.urls import path
from . import views

urlpatterns = [
    path('', views.papers),
    path('papers/', views.papers, name='papers_index'),
    path('persons/', views.persons, name='persons_index'),
    path('paper/<int:id>/', views.paper_detail, name='paper_detail'),
    path('build', views.build, name='build_db'),
]


# for updating/creating a new Paper node
urlpatterns += [
    path('paper/<int:id>/update', views.paper_update, name='paper_update'),
    path('paper/<int:id>/connect/venue', views.paper_connect_venue, name='paper_connect_venue'),
    path('paper/create/', views.paper_create, name='paper_create'),
]

# for updating/creating a new Person node
urlpatterns += [
    path('person/create/', views.person_create, name='person_create'),
    path('person/<int:id>/', views.person_detail, name='person_detail'),
    path('person/<int:id>/update', views.person_update, name='person_update'),
]

# for updating/creating a new Dataset node
urlpatterns += [
    path('datasets/', views.datasets, name='datasets_index'),
    path('dataset/create/', views.dataset_create, name='dataset_create'),
    path('dataset/<int:id>/', views.dataset_detail, name='dataset_detail'),
    path('dataset/<int:id>/update', views.dataset_update, name='dataset_update'),
]

# for updating/creating a new Venue node
urlpatterns += [
    path('venues/', views.venues, name='venues_index'),
    path('venue/create/', views.venue_create, name='venue_create'),
    path('venue/<int:id>/', views.venue_detail, name='venue_detail'),
    path('venue/<int:id>/update', views.venue_update, name='venue_update'),
]

# for updating/creating a new Comment node
urlpatterns += [
    path('comments/', views.comments, name='comments_index'),
    path('comment/create/', views.comment_create, name='comment_create'),
    path('comment/<int:id>/', views.comment_detail, name='comment_detail'),
    path('comment/<int:id>/update', views.comment_update, name='comment_update'),
]