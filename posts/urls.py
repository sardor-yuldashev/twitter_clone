from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('post/', views.post, name='post'),
    path('edit/<int:post_id>/', views.edit, name='edit'),
    path('edit/<int:post_id>/save/', views.save, name='save'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('post_like/<int:post_id>/', views.post_like, name='post_like'),
    path('debug/', views.debug, name='debug'),
]