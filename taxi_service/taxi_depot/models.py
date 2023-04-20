from django.db import models
from datetime import date


class Driver(models.Model):
    driver_name = models.CharField(max_length=20)
    birthday = models.DateField()
    registered_on = models.DateTimeField(auto_now_add=True)
    reg_doc_number = models.CharField(max_length=9, unique=True)
    photo = models.ImageField(upload_to='img/')
    free = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.driver_name}, {self.reg_doc_number}'

    def get_age(self):
        age = int((date.today() - self.birthday).days / 365.20)
        return age


class CarColor(models.Model):
    color_name = models.CharField(max_length=20)

    def __str__(self):
        return self.color_name


class CarBodyType(models.Model):
    body_type = models.CharField(max_length=20)

    def __str__(self):
        return self.body_type


class Manufacturer(models.Model):
    title = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.title


class CarModel(models.Model):
    title = models.CharField(max_length=20)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    weight = models.IntegerField()
    body_type = models.ForeignKey(CarBodyType, on_delete=models.CASCADE)
    engine_capacity = models.FloatField()
    engine_power = models.IntegerField()

    def __str__(self):
        return f'{self.title}//{self.manufacturer}'


class Car(models.Model):
    production_year = models.IntegerField()
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='img/')
    color = models.ForeignKey(CarColor, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=9, unique=True)
    drivers = models.ManyToManyField(Driver, related_name='cars')
    free = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.model}, {self.reg_number}'
