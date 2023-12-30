from django.test import TestCase
from django.utils import timezone
import datetime

from .models import Post, UserLikePost, GeneralInformation, PersonalInformation
from django.contrib.auth import get_user_model
from home.models import GENDERS, COUNTRY_NAMES

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

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


class ProfileCreationTestCase(TestCase):
    # dummy user details
    USER_EMAIL = "test@gmail.com"
    USER_PASSWORD = "test123"
    user = None

    # dummy data for general information
    about_me = "A software engineer is a problem-solving professional proficient in languages like C++. They excel in algorithmic thinking, data structures, and coding, collaborating within teams to create reliable, innovative solutions. Adaptability and a commitment to continuous learning are vital in this rapidly evolving field."
    education = "MIT"
    gender = GENDERS[0][0] # Male
    date_of_birth = datetime.date(year=2002, month=3, day=12)
    organization = "google"
    nationality = COUNTRY_NAMES[0][0]

    # dummy data for personal information
    first_name = "Kevin"
    last_name = "Smith"
    occupation = "Software engineer"
    status = "Busy on working !!"
    location = "New Delhi, Delhi"
    home_address = "home, street no., pincode"
    phone_number = "9876543210"


    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(email=self.USER_EMAIL, password=self.USER_PASSWORD)

    def test_for_creating_general_information_record(self):
        """
        Creating a simple object for the GeneralInformation model
        """
        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        general_information = GeneralInformation.objects.create(user=user, about_me=self.about_me, education=self.education, gender=self.gender, date_of_birth=self.date_of_birth, organization=self.organization, nationality=self.nationality)

        self.assertEqual(general_information.about_me, self.about_me)
        self.assertEqual(general_information.education, self.education)
        self.assertEqual(general_information.gender, self.gender)
        self.assertEqual(general_information.organization, self.organization)
        self.assertEqual(general_information.date_of_birth, self.date_of_birth)
        self.assertEqual(general_information.nationality, self.nationality)
        self.assertEqual(general_information.created_at.strftime(DATE_TIME_FORMAT), general_information.updated_at.strftime(DATE_TIME_FORMAT)) # during first time creation create_at and updated_at should be same


    def test_for_creating_multiple_general_information_records(self):
        """
        Trying to create two GeneralInformation records for the same user and this should through a error.
        """

        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        # first record for user
        GeneralInformation.objects.create(user=user, about_me=self.about_me)

        # second record for user, where it should throw an error or exception
        with self.assertRaises(Exception):
            GeneralInformation.objects.create(user=user, about_me=self.about_me)


    def test_for_creating_general_information_without_user(self):
        """
        Trying to create a GeneralInformation record without user field and this should throw an error.
        """

        # creating GeneralInformation record without about_me field
        with self.assertRaises(Exception):
            GeneralInformation.objects.create()

    def test_for_creating_personal_information_record(self):
        """
        Creating a simple PersonalInformation record.
        """

        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        # creating personal information record for user
        personal_information = PersonalInformation.objects.create(user=user, first_name=self.first_name, last_name=self.last_name, occupation=self.occupation, status=self.status, location=self.location, home_address=self.home_address, phone_number=self.phone_number)

        self.assertEqual(personal_information.first_name, self.first_name)
        self.assertEqual(personal_information.last_name, self.last_name)
        self.assertEqual(personal_information.occupation, self.occupation)
        self.assertEqual(personal_information.status, self.status)
        self.assertEqual(personal_information.location, self.location)
        self.assertEqual(personal_information.home_address, self.home_address)
        self.assertEqual(personal_information.phone_number, self.phone_number)

        self.assertEqual(personal_information.created_at.strftime(DATE_TIME_FORMAT), personal_information.updated_at.strftime(DATE_TIME_FORMAT))

    def test_for_creating_multiple_personal_information_record(self):
        """
        Trying to create multiple PersonalInformation record for same user and it should throw an error
        """

        User = get_user_model()
        user = User.objects.get(email=self.USER_EMAIL)

        # creating first personal information record
        PersonalInformation.objects.create(user=user)

        # creating second personal information record which will throw error
        with self.assertRaises(Exception):
            PersonalInformation.objects.create(user=user)

    def test_for_creating_personal_information_without_user(self):
        """
        Trying to create a PersonalInformation record without user and this should throw an error.
        """

        # creating personal information record without user
        with self.assertRaises(Exception):
            PersonalInformation.objects.create()

    




