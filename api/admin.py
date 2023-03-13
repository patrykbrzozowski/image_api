from django.contrib import admin
from .models import Image, User, Tier

class ImageAdmin(admin.ModelAdmin):
    list_display=['id','image','user']

class UserAdmin(admin.ModelAdmin):
    list_display=['username','tier']

admin.site.register(User, UserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tier)