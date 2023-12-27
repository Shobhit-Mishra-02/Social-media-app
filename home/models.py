from django.db import models
from django.utils import timezone
from authentication.models import AccountUser

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)

    created_at = models.DateTimeField(default=timezone.now())

    image = models.ImageField(upload_to="images", blank=True)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.title
    
class UserLikePost(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self) -> str:
        return f"{self.user.email} likes {self.post.title}"
