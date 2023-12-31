from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Blog, Post, Like
from .forms import BlogForm, PostForm

# Create your views here.
def index(request):
    """The home page for blogs."""
    posts = Post.objects.order_by('-date_added')
    blogs = Blog.objects.all()
    context = {'posts':posts, 'blogs':blogs}
    return render(request, 'blogs/index.html', context)

def blogs(request):
    """The blogs page."""
    blogs = Blog.objects.order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)

def user_blogs(request):
    """The blogs page."""
    blogs = Blog.objects.order_by('date_added').filter(owner=request.user)
    context = {'blogs': blogs}
    return render(request, 'blogs/user_blogs.html', context)

def blog(request, blog_id):
    """Single blog page."""
    blog = Blog.objects.get(id=blog_id)
    posts = blog.post_set.order_by('-date_added')
    context = {'blog':blog, 'posts':posts}
    return render(request, 'blogs/blog.html', context)

@login_required
def new_blog(request):
    """Add a new blog."""
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = BlogForm()
    else:
        # POST data submitted; process data.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:blogs')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

@login_required
def new_post(request, blog_id):
    """Add a new post for a particular blog."""
    blog = Blog.objects.get(id=blog_id)
    check_blog_owner(request, blog)

    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)
    # Display a blank or invalid form
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit a particular post."""
    post = Post.objects.get(id=post_id)
    blog = post.blog
    check_blog_owner(request, blog)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current post.
        form = PostForm(instance=post)
    else:
        # Post data submitted
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)
    
    context = {'post':post, 'blog':blog, 'form':form}
    return render(request, 'blogs/edit_post.html', context)

@login_required
def like_post(request, post_id):
    """Allows the user to like a post if they are logged in and haven't already 
    liked the post."""
    post = Post.objects.get(id=post_id)
    user = request.user
    if Like.objects.filter(user=user, post=post).exists():
        pass
    else:
        Like.objects.create(user=user, post=post)

@login_required
def delete_blog(request, blog_id):
    """Delete a blog."""
    blog = Blog.objects.get(id=blog_id)
    check_blog_owner(request, blog)
    if request.method == 'POST':
        blog.delete()
        return redirect('blogs:blogs')
    context = {'blog':blog}
    return render(request, 'blogs/delete_blog.html', context)

@login_required
def delete_post(request, post_id):
    """Delete a post."""
    post = Post.objects.get(id=post_id)
    blog = post.blog
    check_blog_owner(request, blog)
    if request.method == 'POST':
        post.delete()
        return redirect('blogs:blog', blog_id=blog.id)
    context = {'post':post, 'blog':blog}
    return render(request, 'blogs/delete_post.html', context)

def check_blog_owner(request, blog):
    """Check if the user is the blog owner."""
    if blog.owner != request.user:
        raise Http404