from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from home.models import Post
from .serializers import PostModelSerializer


@csrf_exempt
@login_required
def get_posts(request, page=1):

    if request.method == "GET":

        end_index = page*3
        start_index = end_index - 3

        number_of_posts = Post.objects.all().count()
        total_pages = number_of_posts%3 if number_of_posts/3 +1 else number_of_posts/3 

        posts = Post.objects.all().order_by('-created_at')[start_index:end_index]

        serialized = PostModelSerializer(posts, many=True, context={"request":request})
        serialized_posts = serialized.data

        return JsonResponse(serialized_posts, safe=False)
    
    return JsonResponse({"message":"Invalid request"}, status=500)

@csrf_exempt
@login_required
def increment_likes(request, id):

    if request.method == "GET":

        post = Post.objects.get(pk = id)
        post.total_likes += 1
        post.save()

        return JsonResponse({"message": "done", "total_likes":post.total_likes}, status=200)
    
    return JsonResponse({"message":"Invalid request"}, status=500)