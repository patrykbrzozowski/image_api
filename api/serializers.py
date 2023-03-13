from rest_framework import serializers
from .models import Image, Tier

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('__all__')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

    def get_image_url(self, request, image):
        image_url = image.image.url
        return request.build_absolute_uri(image_url)
    
    def get_image200_url(self, request, image):
        image200_url = image.image_200.url
        return request.build_absolute_uri(image200_url)
    
    def get_image400_url(self, request, image):
        image400_url = image.image_400.url
        return request.build_absolute_uri(image400_url)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        image200_url = self.get_image200_url(request, instance)
        data = {
            "id": instance.id,
            "image200_url": image200_url
        }

        if request.user.tier.link_to_thumbnail400_file:
            image400_url = self.get_image400_url(request, instance)
            data['image400_url'] = image400_url
        
        if request.user.tier.link_to_original_file:
            image_url = self.get_image_url(request, instance)
            data['image_url'] = image_url
        
        return data
    
class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']
