from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .serializers import PostModelSerializer


@csrf_exempt
@login_required
def get_posts(request):

    if request.method == "POST":
        
        user_posts = request.user.post_set.all()
        serialized = PostModelSerializer(user_posts, many=True)
        serialized_posts = serialized.data

        return JsonResponse(serialized_posts, safe=False)
    
    return JsonResponse({"message":"Invalid request"}, status=200)
