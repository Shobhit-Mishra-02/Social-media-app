from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mysite.settings import MEDIA_ROOT

from home.models import Post, GeneralInformation, PersonalInformation
from .serializers import PostModelSerializer, GeneralInformationModelSerializer, PersonalInformationSerializer
from home.forms import PersonalInformationForm, GeneralInformationForm


def handle_upload(f):
    with open(f"{MEDIA_ROOT}/images/{f}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
@login_required
def get_posts(request, page=1):

    if request.method == "GET":

        end_index = page*3
        start_index = end_index - 3

        number_of_posts = Post.objects.all().count()
        total_pages = number_of_posts % 3 if number_of_posts/3 + 1 else number_of_posts/3

        posts = Post.objects.all().order_by(
            '-created_at')[start_index:end_index]

        serialized = PostModelSerializer(
            posts, many=True, context={"request": request})
        serialized_posts = serialized.data

        return JsonResponse(serialized_posts, safe=False)

    return JsonResponse({"message": "Invalid request"}, status=500)


@csrf_exempt
@login_required
def update_like_status(request, id):

    if request.method == "GET":
        user = request.user
        post = Post.objects.get(pk=id)

        if post.userlikepost_set.filter(user=user.id).count():
            # remove user
            post.userlikepost_set.get(user=user.id).delete()
            return JsonResponse({"message": "User removed from like list.", "new_status": False, "new_like_count": post.userlikepost_set.count()})
        else:
            # add user
            post.userlikepost_set.create(user=user, post=post)
            return JsonResponse({"message": "User added in like list.", "new_status": True, "new_like_count": post.userlikepost_set.count()})

    return JsonResponse({"message": "Invalid request"}, status=500)


@csrf_exempt
@login_required
def add_general_information(request):

    form = GeneralInformationForm(
        request.POST, instance=GeneralInformation(user=request.user))

    if request.method == "POST" and form.is_valid():
        about_me = form.cleaned_data["about_me"]
        education = form.cleaned_data["education"]
        gender = form.cleaned_data["gender"]
        date_of_birth = form.cleaned_data["date_of_birth"]
        organization = form.cleaned_data["organization"]
        nationality = form.cleaned_data["nationality"]

        if GeneralInformation.objects.filter(user_id=request.user.id).count():
            GeneralInformation.objects.filter(user_id=request.user.id).update(
                about_me=about_me, education=education, gender=gender, date_of_birth=date_of_birth, organization=organization, nationality=nationality)

            data = GeneralInformation.objects.get(user_id=request.user.id)
            serialized_data = GeneralInformationModelSerializer(data).data
            return JsonResponse(serialized_data)
        else:
            form.save()

            data = GeneralInformation.objects.get(user_id=request.user.id)
            serialized_data = GeneralInformationModelSerializer(data).data
            return JsonResponse(serialized_data)

    return JsonResponse({"message": "invalid method"})


@csrf_exempt
@login_required
def add_personal_information(request):

    if request.method == "POST":
        
        if PersonalInformation.objects.filter(user_id=request.user.id).count()>0:
            instance = PersonalInformation.objects.get(user_id=request.user.id)
            form = PersonalInformationForm(request.POST, request.FILES, instance=instance)

            if form.is_valid():
                form.save()
            else:
                return JsonResponse({"message":"Form is not valid"}, status=500)
        else:
            form = PersonalInformationForm(request.POST, request.FILES)
            
            if form.is_valid():
                form.save()
            else:
                return JsonResponse({"message":"Form is not valid"}, status=500)
            
        data = PersonalInformation.objects.get(user_id=request.user.id)
        serialized_data = PersonalInformationSerializer(data, context={"request": request}).data

        return JsonResponse(serialized_data, status=200)

    return JsonResponse({"message":"Invalid method"}, status=500)



@csrf_exempt
@login_required
def get_general_information(request):
    if request.method == "GET":
        general_information = GeneralInformation.objects.filter(
            user_id=request.user.id)

        if len(general_information) > 0:
            serialized_general_information = GeneralInformationModelSerializer(
                general_information[0]).data
            return JsonResponse(serialized_general_information, status=200)

        return JsonResponse({"message": "No data found"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def get_personal_information(request):
    if request.method == "GET":
        personal_information = PersonalInformation.objects.filter(
            user_id=request.user.id)

        if len(personal_information) > 0:

            serialized_personal_information = PersonalInformationSerializer(
                personal_information[0], context={"request": request}).data

            return JsonResponse(serialized_personal_information, status=200)

        return JsonResponse({"message": "No data found"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)
