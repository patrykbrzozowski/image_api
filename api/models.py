from django.db import models
from django.contrib.auth.models import User, AbstractUser

from .helpers import make_thumbnail
from .validators import validate_file_extension

class Tier(models.Model):
    name = models.CharField(max_length=200)
    link_to_thumbnail200_file = models.BooleanField(default=True)
    link_to_thumbnail400_file = models.BooleanField(default=False)
    link_to_original_file = models.BooleanField(default=False)
    generate_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT, related_name='tier', default=1)

class Image(models.Model):
    def nameFile(instance, file_name):
        return '/'.join(['images', file_name])
    
    image = models.ImageField(upload_to=nameFile)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image_200 = models.ImageField(upload_to='images/thumbnails_200', blank=True)
    image_400 = models.ImageField(upload_to='images/thumbnails_400', blank=True)
    
    def save(self, *args, **kwargs):
        validate_file_extension(self.image)
        make_thumbnail(self.image_200, self.image, (200, 200), 'thumb200')
        make_thumbnail(self.image_400, self.image, (400, 400), 'thumb400')
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.name
