from django.urls import path
from . import views

urlpatterns = [
    path('', views.papers),
    path('papers/', views.papers, name='papers_index'),
    path('authors/', views.authors, name='authors_index'),
    path('paper/<int:id>/', views.paper_detail, name='paper_detail'),
    path('build', views.build, name='build_db'),
]


# for creating a new Paper node
urlpatterns += [
    path('paper/<int:id>/update', views.paper_update, name='paper_update'),
]

urlpatterns += [
    path('author/create/', views.author_create, name='author_create'),
]