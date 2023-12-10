from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_exempt
@login_required
def get_posts(request):

    if request.method == "POST":
        
        user_posts = request.user.post_set.all()

        data = json.loads(request.body.decode('utf-8'))

        response_data = {'message':'Hello from the server !!', 'data': data}

        return JsonResponse(response_data)
    
    return JsonResponse({"message":"Invalid request"}, status=200)
