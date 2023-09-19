from django.db import models

# Create your models here.
class Blog(models.Model):
    """An overall blog."""
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

class Post(models.Model):
    """A single post within an overall blog."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'posts'
    
    def __str__(self):
        """Return a string representation of the post."""
        return f"{self.text}"