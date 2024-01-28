from rest_framework import serializers
from home.models import Post, GeneralInformation, PersonalInformation
from authentication.models import AccountUser


class PostModelSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    did_user_like_post = serializers.SerializerMethodField()
    owner_full_name = serializers.SerializerMethodField()
    owner_profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created_at', 'image_url', 'caption',
                  'total_likes', 'did_user_like_post', 'owner_full_name', 'owner_profile_pic')

    def get_owner_full_name(self, post):

        records = PersonalInformation.objects.filter(user_id=post.user.id)

        if records.count() > 0:
            personal_information = records[0]

            return personal_information.first_name + " " + personal_information.last_name

        return "name_not_found"

    def get_owner_profile_pic(self, post):
        request = self.context.get('request')
        records = PersonalInformation.objects.filter(user_id=post.user.id)

        if records.count() > 0:
            personal_information = records[0]

            if personal_information.profile_pic and hasattr(personal_information.profile_pic, 'url'):
                image_url = personal_information.profile_pic.url
                return request.build_absolute_uri(image_url)

        return None

    def get_image_url(self, post):
        request = self.context.get('request')

        if post.image and hasattr(post.image, 'url'):
            image_url = post.image.url
            return request.build_absolute_uri(image_url)

        return None

    def get_total_likes(self, post):
        return post.userlikepost_set.count()

    def get_did_user_like_post(self, post):
        request = self.context.get("request")
        user_id = request.user.id
        return True if post.userlikepost_set.filter(user=user_id).count() else False


class GeneralInformationModelSerializer(serializers.ModelSerializer):

    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = GeneralInformation
        fields = "__all__"
        extra_fields = ["is_owner"]

    def get_is_owner(self, general_information):
        request = self.context.get("request")

        if request.user.id == general_information.user.id:
            return True

        return False


class PersonalInformationSerializer(serializers.ModelSerializer):

    profile_pic = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInformation
        fields = "__all__"

    def get_profile_pic(self, personal_information):
        request = self.context.get('request')

        if personal_information.profile_pic and hasattr(personal_information.profile_pic, 'url'):
            image_url = personal_information.profile_pic.url
            return request.build_absolute_uri(image_url)

        return None

    def get_is_owner(self, personal_information):
        request = self.context.get('request')

        if personal_information.user.id == request.user.id:
            return True

        return False

    def get_full_name(self, personal_information):
        full_name = ""

        if personal_information.first_name:
            full_name = personal_information.first_name

        if personal_information.last_name:
            full_name = full_name + " " + personal_information.last_name

        return full_name.title()

    def get_email(self, personal_information):
        return personal_information.user.email


class AccountUserModelSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = AccountUser
        fields = ["date_joined", "email", "username",
                  "id", "first_name", "last_name", "profile_pic"]

    def get_first_name(self, user):
        personal_information = PersonalInformation.objects.filter(
            user_id=user.id).first()

        if personal_information:
            return personal_information.first_name

        return None

    def get_last_name(self, user):
        personal_information = PersonalInformation.objects.filter(
            user_id=user.id).first()

        if personal_information:
            return personal_information.last_name

        return None

    def get_profile_pic(self, user):
        request = self.context.get('request')

        personal_information = PersonalInformation.objects.filter(
            user_id=user.id).first()

        if personal_information is None:
            return None

        if personal_information.profile_pic and hasattr(personal_information.profile_pic, 'url'):
            image_url = personal_information.profile_pic.url
            return request.build_absolute_uri(image_url)

        return None


class TrendingPostSerializer(serializers.ModelSerializer):

    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_like_count(self, post):
        return post.like_count
