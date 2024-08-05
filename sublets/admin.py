from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, ListingPicture, Message
from .models import UserProfile, ProfilePicture

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(ListingPicture)
admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(ProfilePicture)