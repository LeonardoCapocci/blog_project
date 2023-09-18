from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm

# Create your views here.
def index(request):
    """The home page for blogs."""
    return render(request, 'blogs/index.html')

def blogs(request):
    """The blogs page."""
    blogs = Blog.objects.order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)

def blog(request, blog_id):
    """Single blog page."""
    blog = Blog.objects.get(id=blog_id)
    posts = blog.post_set.order_by('-date_added')
    context = {'blog':blog, 'posts':posts}
    return render(request, 'blogs/blog.html', context)

def new_blog(request):
    """Add a new blog."""
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = BlogForm()
    else:
        # POST data submitted; process data.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogs')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)