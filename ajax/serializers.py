from rest_framework import serializers
from home.models import Post

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'