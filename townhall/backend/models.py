import socket
import secrets
from django.db import models

def generate_default_id():
    """Generate a default unique identifier."""
    return secrets.token_urlsafe(8)

class BaseModel(models.Model):
    """Abstract base model to include common fields and methods."""
    id = models.CharField(primary_key=True, max_length=16, unique=True, default=generate_default_id)

    class Meta:
        abstract = True

    @classmethod
    def get_and_save_ip(cls):
        """Get and save the IP address of the instance."""
        ip_address = socket.gethostbyname(socket.gethostname())
        if ip_address:
            instance = cls(ip_address=ip_address)
            instance.save()
            return instance

class User(BaseModel):
    """User model representing a system user."""
    ip_address = models.CharField(max_length=15, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class Category(BaseModel):
    """Category model for organizing posts."""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Post(BaseModel):
    """Post model representing blog or forum posts."""
    title = models.CharField(max_length=15)
    body = models.CharField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)  # Optional image field

    def __str__(self):
        return self.title

class Comment(BaseModel):
    """Comment model for comments on posts."""
    body = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
