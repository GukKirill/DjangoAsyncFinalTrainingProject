from django.urls import path
from .views import *


urlpatterns = [
    path('drivers/', drivers, name='drivers'),
    path('cars/', cars, name='cars'),
    path('driver/<int:pk>/', drivers_profile, name='drivers_profile'),
    path('cars/<int:pk>/', cars_profile, name='cars_profile'),
]
