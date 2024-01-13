from rest_framework import serializers
from home.models import Post, GeneralInformation, PersonalInformation

class PostModelSerializer(serializers.ModelSerializer):
    
    image_url = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    did_user_like_post = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'created_at', 'image_url', 'caption', 'total_likes', 'did_user_like_post')

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

    class Meta:
        model = PersonalInformation
        fields = "__all__"