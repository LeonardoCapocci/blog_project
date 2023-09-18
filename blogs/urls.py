"""Defines URL patterns for blogs."""

from django.urls import path
from . import views

app_name = "blogs"
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page thats shows all the blogs.
    path('blogs/', views.blogs, name='blogs'),
    # Page for a specific blog.
    path('blogs/<int:blog_id>/', views.blog, name='blog'),
    # Page for adding a new blog.
    path('new_blog/', views.new_blog, name='new_blog'),
    # Page for adding a new post.
    path('new_post/<int:blog_id>/', views.new_post, name='new_post')
]
