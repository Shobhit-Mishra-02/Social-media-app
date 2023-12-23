from rest_framework import serializers
from home.models import Post

class PostModelSerializer(serializers.ModelSerializer):
    
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'total_likes', 'created_at', 'image_url', 'caption')

    def get_image_url(self, post):
        request = self.context.get('request')
        
        if post.image and hasattr(post.image, 'url'):
            image_url = post.image.url 
            return request.build_absolute_uri(image_url)
        
        return None

       