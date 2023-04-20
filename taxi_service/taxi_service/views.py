from asgiref.sync import sync_to_async
from django.shortcuts import render


async def home(request):
    return await sync_to_async(render)(request, 'home.html')
