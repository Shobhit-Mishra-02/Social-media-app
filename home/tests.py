from django.test import TestCase

from .models import Post
from django.contrib.auth import get_user_model

# Create your tests here.
class PostTetsCase(TestCase):
    # dummy user details
    USER_EMAIL = "test@gmail.com"
    USER_PASSWORD = "test123"

    # dummy post details
    POST_TITLE = "post title"
    POST_CONTENT = "Post content"

    
    def setUp(self) -> None:
        User = get_user_model()
        User.objects.create(email=self.USER_EMAIL, password=self.USER_PASSWORD)

    def test_for_post_creation(self):
        "Test case for simple post creation."
        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        post = Post.objects.create(user=user, title=self.POST_TITLE, content=self.POST_CONTENT)

        self.assertEqual(post.title, self.POST_TITLE)
        self.assertEqual(post.content, self.POST_CONTENT)

