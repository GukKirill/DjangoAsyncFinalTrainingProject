from django.urls import path
from .views import *

urlpatterns = [
    path('choose_driver/car-<int:pk>/', choose_driver, name='choose_driver'),
    path('choose_car/driver-<int:pk>/', choose_car, name='choose_car'),
    path('choose_route/driver-<int:driver_pk>car-<int:car_pk>/', choose_route, name='choose_route'),
    path('trip_confirmation/<int:driver_pk>-<int:car_pk>-<start>-<end>-<int:cost>', trip_confirmation, name='trip_confirmation'),
]
