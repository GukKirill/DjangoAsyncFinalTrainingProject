from django.db import models
from taxi_depot.models import Driver, Car
from django.contrib.auth.models import User


class Trip(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    start_point = models.CharField(max_length=20)
    end_point = models.CharField(max_length=20)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.start.strftime("%d-%m-%y %H:%M")} - {self.end.strftime("%d-%m-%y %H:%M")} | ' \
               f'{self.start_point} - {self.end_point} | {self.cost}'
