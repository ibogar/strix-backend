from django.db import models

from users.models import User
from posts.models import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)