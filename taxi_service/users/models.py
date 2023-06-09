from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='profile_pics/default_user.jpg',
        upload_to='profile_pics'
    )

    def save(self, **kwargs):
        super().save(**kwargs)
        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'
