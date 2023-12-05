from django.db import models
from django.utils import timezone
from authentication.models import AccountUser

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(blank=False)

    total_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now())

    image = models.ImageField(upload_to="images", blank=True)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.title
