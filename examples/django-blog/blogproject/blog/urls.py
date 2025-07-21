"""
URL configuration for the blog application.
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/',
         views.CategoryDetailView.as_view(), name='category_detail'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('search/', views.search_posts, name='search'),
    path('about/', views.about, name='about'),

    # API endpoints
    path('api/posts/', views.api_posts, name='api_posts'),
    path('api/categories/', views.api_categories, name='api_categories'),
]
