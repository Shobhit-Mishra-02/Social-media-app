from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from home.models import Post
from .serializers import PostModelSerializer


'''
REQUEST
The front part will send the body with 'request_page' value and it contains the requested page number
post_body = {
    requested_page: 1
}

RESPONSE
After getting the requested page number the required data is generated like this
response = {
    total_pages:2,
    page_number: 1,
    post_number: 3,
    posts:[
    {title, content, created_at, image, caption, email, username},
    {title, content, created_at, image, caption, email, username},
    {title, content, created_at, image, caption, email, username},
    ]
}
'''

@csrf_exempt
@login_required
def get_posts(request):

    if request.method == "POST":
        page_numer = request.POST['requested_page']
        
        end_index = page_numer*3
        start_index = end_index - 3

        number_of_posts = Post.objects.all().count()

        posts = Post.objects.all().order_by('-created_at')[start_index:end_index]

        serialized = PostModelSerializer(posts, many=True)
        serialized_posts = serialized.data

        return JsonResponse(serialized_posts, safe=False)
    
    return JsonResponse({"message":"Invalid request"}, status=200)
