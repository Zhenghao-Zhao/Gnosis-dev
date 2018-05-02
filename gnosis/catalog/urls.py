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
    path('paper/create/', views.paper_create, name='paper_create'),
]

# for updating/creating a new Person node
urlpatterns += [
    path('person/create/', views.person_create, name='person_create'),
]