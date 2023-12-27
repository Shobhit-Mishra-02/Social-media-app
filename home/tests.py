from django.test import TestCase
from django.utils import timezone
import datetime

from .models import Post, UserLikePost
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
        """
        Test case for simple post creation.
        """
        today =  timezone.now()
        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        # Creating a new post
        post = Post.objects.create(user=user, title=self.POST_TITLE, content=self.POST_CONTENT)

        self.assertEqual(post.title, self.POST_TITLE)
        self.assertEqual(post.content, self.POST_CONTENT)

        self.assertEqual(post.created_at.year, today.year)
        self.assertEqual(post.created_at.day, today.day)

    def test_post_creation_for_custome_datetime(self):
        """
        Testing case for creating post where we try to manipulate created_at field
        """
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        today = timezone.now()
        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        # Creating a new post with tomorrow created_at time
        Post.objects.create(user=user, title=self.POST_TITLE, content=self.POST_CONTENT)



    def test_for_post_like_count(self):
        """
        Test for post like count
        """
        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        # Creating a new post
        post = Post.objects.create(user=user, title=self.POST_TITLE, content=self.POST_CONTENT)

        # default count should be zero
        self.assertEqual(post.userlikepost_set.count(), 0, 'Post like count is not zero !!')

        # creating a like record in UserLikePost model
        UserLikePost.objects.create(user=user, post=post)

        # after liking the post
        self.assertEqual(post.userlikepost_set.count(), 1, 'Post like count after one record in the UserLikePost table')


    

