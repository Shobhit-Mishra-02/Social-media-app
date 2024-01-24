from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from home.models import Post, GeneralInformation, PersonalInformation
from .serializers import PostModelSerializer, GeneralInformationModelSerializer, PersonalInformationSerializer, AccountUserModelSerializer, TrendingPostSerializer
from home.forms import PersonalInformationForm, GeneralInformationForm, PostCreationForm
from authentication.models import AccountUser


@csrf_exempt
@login_required
def get_posts(request, page=1, own_user=0):

    if request.method == "GET":

        end_index = page*3
        start_index = end_index - 3

        if own_user == 0:
            posts = Post.objects.all().order_by(
                '-created_at')[start_index:end_index]
        else:
            posts = Post.objects.filter(user_id=request.user.id).order_by(
                '-created_at')[start_index:end_index]

        serialized = PostModelSerializer(
            posts, many=True, context={"request": request})
        serialized_posts = serialized.data

        return JsonResponse(serialized_posts, safe=False)

    return JsonResponse({"message": "Invalid request"}, status=500)


@csrf_exempt
@login_required
def get_post(request, id):
    if request.method == "GET":
        try:
            post = Post.objects.get(pk=id)
            serialized_post = PostModelSerializer(
                post, context={"request": request}).data
            return JsonResponse(serialized_post)
        except Exception:
            return JsonResponse({"message": "Post not found"}, status=404)

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

        if PersonalInformation.objects.filter(user_id=request.user.id).count() > 0:
            instance = PersonalInformation.objects.get(user_id=request.user.id)
            form = PersonalInformationForm(
                request.POST, request.FILES, instance=instance)

            if form.is_valid():
                form.save()
            else:
                return JsonResponse({"message": "Form is not valid"}, status=500)
        else:
            instance = PersonalInformation(user=request.user)
            form = PersonalInformationForm(
                request.POST, request.FILES, instance=instance)

            if form.is_valid():
                form.save()
            else:
                return JsonResponse({"message": "Form is not valid"}, status=500)

        data = PersonalInformation.objects.get(user_id=request.user.id)
        serialized_data = PersonalInformationSerializer(
            data, context={"request": request}).data

        return JsonResponse(serialized_data, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def get_general_information(request, id):
    if request.method == "GET":
        general_information = GeneralInformation.objects.filter(
            user_id=id)

        if len(general_information) > 0:
            serialized_general_information = GeneralInformationModelSerializer(
                general_information[0]).data
            return JsonResponse(serialized_general_information, status=200)

        return JsonResponse({"message": "No data found"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def get_personal_information(request, id):
    if request.method == "GET":
        personal_information = PersonalInformation.objects.filter(
            user_id=id)

        if len(personal_information) > 0:

            serialized_personal_information = PersonalInformationSerializer(
                personal_information[0], context={"request": request}).data

            return JsonResponse(serialized_personal_information, status=200)

        return JsonResponse({"message": "No data found"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def get_user_details(request, id):
    if request.method == "GET":
        users = AccountUser.objects.filter(pk=id)

        response = {}

        if users.count() > 0:
            serialized_user = AccountUserModelSerializer(
                users[0], context={"request": request}).data
            response["user"] = serialized_user
        else:
            return JsonResponse({"message": "User does not exist"}, status=500)

        personal_informations = PersonalInformation.objects.filter(user_id=id)

        if personal_informations.count() > 0:
            serialized_personal_information = PersonalInformationSerializer(
                personal_informations[0]).data
            response["personal_information"] = serialized_personal_information
        else:
            response["personal_information"] = PersonalInformationSerializer(
                PersonalInformation(user=users[0])).data

        general_informations = GeneralInformation.objects.filter(user_id=id)

        if general_informations.count() > 0:
            serialized_general_information = GeneralInformationModelSerializer(
                general_informations[0]).data
            response["general_information"] = serialized_general_information
        else:
            response["general_information"] = GeneralInformationModelSerializer(
                GeneralInformation(user=users[0])).data

        return JsonResponse(response, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def get_trending_posts(request):
    if request.method == "GET":
        response = Post.objects.annotate(like_count=Count(
            "userlikepost__user")).order_by('-like_count')[:5]

        serialized_response = TrendingPostSerializer(response, many=True).data

        return JsonResponse(serialized_response, status=200, safe=False)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def delete_post(request, id):

    if request.method == "GET":
        filtered_post = Post.objects.filter(user_id=request.user.id, id=id)

        if filtered_post.count() > 0:
            post = filtered_post[0]
            post.delete()

            return JsonResponse({"message": "removed the post", "post_id": id}, status=200)
        else:
            return JsonResponse({"message": "Not a valid user"}, status=500)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def update_post(request, id):

    if request.method == "POST":
        post = Post.objects.filter(user_id=request.user.id, id=id).first()

        if post:
            form = PostCreationForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                form.save()
                return JsonResponse({"message": "Updated the post"}, status=200)
            else:
                return JsonResponse({"message": "Data is invalid"}, status=500)

        return JsonResponse({"message": "Post not found"}, status=404)

    return JsonResponse({"message": "Invalid method"}, status=500)


@csrf_exempt
@login_required
def search_users(request):

    if request.method == "POST":
        search_string = request.POST["search_string"]
        users = AccountUser.objects.filter(email__icontains=search_string)
        serialized_data = AccountUserModelSerializer(
            users, many=True, context={"request": request}).data

        return JsonResponse(serialized_data, safe=False)

    return JsonResponse({"message": "Invalid method"}, status=500)
