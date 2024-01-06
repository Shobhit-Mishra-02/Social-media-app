from django.test import TestCase
from home.models import GENDERS, COUNTRY_NAMES, GeneralInformation
import datetime
from django.contrib.auth import get_user_model
from home.forms import GeneralInformationForm


# Create your tests here.

class GeneralInformationFormTestCase(TestCase):

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

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(email=self.USER_EMAIL, password=self.USER_PASSWORD)