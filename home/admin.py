from django.contrib import admin

from .models import *

# registering the models to the admin panel
admin.site.register(Post)
admin.site.register(UserLikePost)

admin.site.register(PersonalInformation)
admin.site.register(GeneralInformation)

admin.site.register(Friend)
admin.site.register(FriendRequest)
