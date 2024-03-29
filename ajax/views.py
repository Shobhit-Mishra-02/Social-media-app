from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from home.models import *
from .serializers import *
from home.forms import PersonalInformationForm, GeneralInformationForm, PostCreationForm
from authentication.models import AccountUser


# contoller to get the posts
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


# controller to get one post by id
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


# controller to get new like status record
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


# controller to add generate information
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
            serialized_data = GeneralInformationModelSerializer(
                data, context={"request": request}).data
            return JsonResponse(serialized_data)
        else:
            form.save()

            data = GeneralInformation.objects.get(user_id=request.user.id)
            serialized_data = GeneralInformationModelSerializer(
                data, context={"request": request}).data
            return JsonResponse(serialized_data)

    return JsonResponse({"message": "invalid method"})


# controller to add personal information
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


# controller to get general information of user by id
@csrf_exempt
@login_required
def get_general_information(request, id):
    if request.method == "GET":
        general_information = GeneralInformation.objects.filter(user_id=id)

        if len(general_information):
            serialized_general_information = GeneralInformationModelSerializer(
                general_information[0], context={"request": request}).data
            return JsonResponse(serialized_general_information, status=200)

        serialized_general_information = GeneralInformationModelSerializer(GeneralInformation(
            user=AccountUser.objects.get(pk=id)), context={"request": request}).data

        return JsonResponse(serialized_general_information, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to get personal information of user by id
@csrf_exempt
@login_required
def get_personal_information(request, id):
    if request.method == "GET":
        personal_information = PersonalInformation.objects.filter(user_id=id)

        if len(personal_information):

            serialized_personal_information = PersonalInformationSerializer(
                personal_information[0], context={"request": request}).data

            return JsonResponse(serialized_personal_information, status=200)

        serialized_personal_information = PersonalInformationSerializer(
            PersonalInformation(user=AccountUser()), context={"request": request}).data

        return JsonResponse(serialized_personal_information, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to get user details by id
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


# controller to get trending posts
@csrf_exempt
@login_required
def get_trending_posts(request):
    if request.method == "GET":
        response = Post.objects.annotate(like_count=Count(
            "userlikepost__user")).order_by('-like_count')[:5]

        serialized_response = TrendingPostSerializer(response, many=True).data

        return JsonResponse(serialized_response, status=200, safe=False)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to delete a post by id
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


# controller to update a post
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


# controller to search the user with given serach_string
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


# controller to make a friend request
@csrf_exempt
@login_required
def make_friend_request(request, id):
    if request.method == "GET":

        sender = request.user
        receiver = AccountUser.objects.filter(pk=id).first()

        # checking for the valid receiver
        if receiver is None:
            return JsonResponse({"message": f"no receiver found with id {id}"}, status=404)

        # searching for prev active friend request, if exists then returning the same.
        prev_friend_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver, pending_status=True).first()

        if prev_friend_request is not None:
            return JsonResponse({"message": "Friend request already exists.", "friend_request": prev_friend_request}, status=200)

        # making a new friend request
        friend_request = FriendRequest.objects.create(
            sender=sender, receiver=receiver)

        serialized_data = FriendRequestModelSerializer(
            friend_request, context={"request": request}).data

        return JsonResponse({"message": "Made a friend request", "friend_request": serialized_data}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to get the friend request status
@csrf_exempt
@login_required
def friend_request_status(request, id):
    if request.method == "GET":

        expected_friend = AccountUser.objects.filter(pk=id).first()

        # checking for valid expected friend
        if expected_friend is None:
            return JsonResponse({"message": f"No user found with id {id}"}, status=400)

        is_friend = False

        # checking for the friend status
        if request.user.friend_ship_records.filter(friend__id=expected_friend.id).count():
            is_friend = True

        # filtering the latest made request by the user to the expected friend
        friend_request = request.user.friend_requests.filter(
            receiver=expected_friend).order_by("-created_at").first()

        # or if the expected friend made the request
        if friend_request is None:
            friend_request = expected_friend.friend_requests.filter(
                receiver=request.user).order_by("-created_at").first()

        serialized_data = None

        # creating serialized data if latest record of friend request exists.
        if friend_request is not None:
            serialized_data = FriendRequestModelSerializer(
                friend_request, context={"request": request}).data

        return JsonResponse({"friend_request": serialized_data, "is_friend": is_friend}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to decline the friend request
@csrf_exempt
@login_required
def declining_request(request, id):
    if request.method == "GET":

        friend_request = FriendRequest.objects.filter(pk=id).first()

        # checking for a valid friend request
        if friend_request is None:
            return JsonResponse({"message": f"friend request {id} does not exist"}, status=404)

        # the user who is rejecting or declining the request should be either sender or receiver.
        if request.user.id != friend_request.receiver.id and request.user.id != friend_request.sender.id:
            return JsonResponse({"message": "You can not decline this friend request"}, status=500)

        friend_request.pending_status = False
        friend_request.declined_status = True
        friend_request.save()

        return JsonResponse({"message": "declined the request"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to accept the friend request
@csrf_exempt
@login_required
def accepting_request(request, id):
    if request.method == "GET":

        friend_request = FriendRequest.objects.filter(pk=id).first()

        # checking for the valid friend request
        if friend_request is None:
            return JsonResponse({"message": f"friend request {id} does not exist"})

        # only the receiver can accept the friend request
        if request.user.id != friend_request.receiver.id:
            return JsonResponse({"message": "You can not accept the friend request"})

        # accepting the friend request
        friend_request.pending_status = False
        friend_request.accept_status = True
        friend_request.save()

        # making friends record
        sender = friend_request.sender
        receiver = friend_request.receiver

        Friend.objects.create(user=sender, friend=receiver)
        Friend.objects.create(user=receiver, friend=sender)

        return JsonResponse({"message": "Request has been accepted"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to get all the friend requests which has been sent to user with given id
# if type is True, then it will return the received friend requests
# if type is False, then it will return the sent friend requests
@csrf_exempt
@login_required
def get_friend_requests(request, id, type):

    if request.method == "GET":
        user = AccountUser.objects.filter(pk=id).first()

        # checking for the valid user
        if user is None:
            return JsonResponse({"message": "user not found"}, status=400)

        # filtering only those received or send friend requests, where pening status is True
        if type:
            friend_requests = user.received_friend_requests.filter(
                pending_status=True)
        else:
            friend_requests = user.friend_requests.filter(pending_status=True)

        serialized_data = FriendRequestModelSerializer(
            friend_requests, many=True, context={"request": request}).data

        return JsonResponse(serialized_data, safe=False, status=200)

    return JsonResponse({"message": "Invalid method"})


# controller to get all the friends of the user with given id
@csrf_exempt
@login_required
def get_friends(request, id):

    if request.method == "GET":

        user = AccountUser.objects.filter(pk=id).first()

        # checking for a valid user
        if user is None:
            return JsonResponse({"message": "User not found"}, status=404)

        friend_ids = user.friend_ship_records.all().values("friend_id")
        friends = AccountUser.objects.filter(id__in=friend_ids)

        serialized_data = AccountUserModelSerializer(
            friends, many=True, context={"request": request}).data

        return JsonResponse(serialized_data, status=200, safe=False)

    return JsonResponse({"message": "Invalid method"}, status=500)


# controller to remove the friend
@csrf_exempt
@login_required
def remove_friend(request, id):
    if request.method == "GET":
        user = request.user
        friend = AccountUser.objects.filter(pk=id).first()

        # checking for a valid friend
        if friend is None:
            return JsonResponse({"message": "Friend does not exist"}, status=404)

        # deleting records from the Friends relation
        Friend.objects.get(user=user, friend=friend).delete()
        Friend.objects.get(user=friend, friend=user).delete()

        return JsonResponse({"message": "Removed the friendship"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=500)
