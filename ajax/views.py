from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from home.models import Post, GeneralInformation, PersonalInformation
from .serializers import PostModelSerializer, GeneralInformationModelSerializer, PersonalInformationSerializer
from home.forms import PersonalInformationForm, GeneralInformationForm

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
def update_like_status(request, id):
    
    if request.method == "GET":
        user = request.user
        post = Post.objects.get(pk=id)
        
        if post.userlikepost_set.filter(user = user.id).count():
            # remove user 
            post.userlikepost_set.get(user = user.id).delete()
            return JsonResponse({"message":"User removed from like list.", "new_status":False, "new_like_count":post.userlikepost_set.count()})
        else:
            # add user
            post.userlikepost_set.create(user=user, post=post)
            return JsonResponse({"message":"User added in like list.", "new_status":True, "new_like_count":post.userlikepost_set.count()})
    
    return JsonResponse({"message":"Invalid request"}, status=500)

@csrf_exempt
@login_required
def add_general_information(request):
    
    form = GeneralInformationForm(request.POST, instance=GeneralInformation(user=request.user))

    if request.method == "POST" and form.is_valid():
        about_me = form.cleaned_data["about_me"]
        education = form.cleaned_data["education"]
        gender = form.cleaned_data["gender"]
        date_of_birth = form.cleaned_data["date_of_birth"]
        organization = form.cleaned_data["organization"]
        nationality = form.cleaned_data["nationality"]

        if GeneralInformation.objects.filter(user_id=request.user.id).count():
            GeneralInformation.objects.filter(user_id=request.user.id).update(about_me=about_me, education=education, gender=gender, date_of_birth=date_of_birth, organization=organization, nationality=nationality)
            return JsonResponse({"message":"Updated the record"})
        else:
            form.save()

            return JsonResponse({"message":"Created a new record"})
    
    return JsonResponse({"message": "invalid method"})

@csrf_exempt
@login_required
def get_general_information(request):
    if request.method == "GET":
        general_information = GeneralInformation.objects.filter(user_id=request.user.id)[0]
        serialized_general_information = GeneralInformationModelSerializer(general_information).data

        return JsonResponse(serialized_general_information, status=200)
    
    return JsonResponse({"message":"Invalid method"}, status=500)

@csrf_exempt
@login_required
def get_personal_information(request):
    if request.method == "GET":
        personal_information = PersonalInformation.objects.filter(user_id=request.user.id)[0]
        serialized_personal_information = PersonalInformationSerializer(personal_information).data

        return JsonResponse(serialized_personal_information, status=200)
    
    return JsonResponse({"message":"Invalid method"}, status=500)
