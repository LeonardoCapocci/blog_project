"""Defines URL patterns for blogs."""

from django.urls import path
from . import views

app_name = "blogs"
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page thats shows all the blogs.
    path('blogs/', views.blogs, name='blogs'),
    # Page that shows the user all their blogs.
    path('user_blogs/', views.user_blogs, name='user_blogs'),
    # Page for a specific blog.
    path('blogs/<int:blog_id>/', views.blog, name='blog'),
    # Page for adding a new blog.
    path('new_blog/', views.new_blog, name='new_blog'),
    # Page for adding a new post.
    path('new_post/<int:blog_id>/', views.new_post, name='new_post'),
    # Page for editing a previous post.
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # Page for deleting a blog.
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    # Page for deleting a post.
    path('delete_pos/<post_id>/', views.delete_post, name='delete_post'),
]