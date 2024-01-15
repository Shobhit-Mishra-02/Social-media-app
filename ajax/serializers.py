from rest_framework import serializers
from home.models import Post, GeneralInformation, PersonalInformation

class PostModelSerializer(serializers.ModelSerializer):
    
    image_url = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    did_user_like_post = serializers.SerializerMethodField()
    owner_full_name = serializers.SerializerMethodField()
    owner_profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created_at', 'image_url', 'caption', 'total_likes', 'did_user_like_post', 'owner_full_name', 'owner_profile_pic')

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
        return True if post.userlikepost_set.filter(user = user_id).count() else False
       
class GeneralInformationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralInformation
        fields = "__all__"

class PersonalInformationSerializer(serializers.ModelSerializer):

    profile_pic = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInformation
        fields = "__all__"

    def get_profile_pic(self, personal_information):
        request = self.context.get('request')
        
        if personal_information.profile_pic and hasattr(personal_information.profile_pic, 'url'):
            image_url = personal_information.profile_pic.url 
            return request.build_absolute_uri(image_url)
        
        return None
    
    def get_full_name(self, personal_information):
        return personal_information.first_name + " " + personal_information.last_name
    
    def get_email(self, personal_information):
        return personal_information.user.email