from django.db import models
from django.contrib.auth.models import User
from trips.models import Trip


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    about_driver = models.TextField(max_length=250, default=None)
    about_car = models.TextField(max_length=250, default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}/ {self.trip}'
