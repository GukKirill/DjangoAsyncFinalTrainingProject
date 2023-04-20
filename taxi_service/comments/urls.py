from django.urls import path
from .views import *

urlpatterns = [
    path('', comment, name='comment'),
    path('update/', comment_update, name='comment_update'),
    path('delete/', comment_delete, name='comment_delete'),
]