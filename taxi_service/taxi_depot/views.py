from django.shortcuts import render
from .models import *
from trips.models import Trip
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from .services import refresh_db


async def drivers(request):
    await refresh_db()
    age_from = 18
    age_to = 56
    drivers_obj = Driver.objects.all()
    if request.method == 'POST':
        if request.POST['age_from']:
            age_from = int(request.POST['age_from'])
        if request.POST['age_to']:
            age_to = int(request.POST['age_to'])
        if age_from > 56 or age_from < 18:
            age_from = 18
        if age_to > 56 or age_to < 18:
            age_to = 56
        drivers_obj_old = drivers_obj
        drivers_obj = []
        async for driver in drivers_obj_old:
            if age_from <= driver.get_age() <= age_to:
                drivers_obj.append(driver)

    context = {
        'drivers': drivers_obj,
        'age_from': age_from,
        'age_to': age_to,
    }
    return await sync_to_async(render)(request, 'drivers.html', context=context)


async def cars(request):
    await refresh_db()
    year_from = date.today().year - 25
    year_to = date.today().year
    cars_obj = Car.objects.all()
    manufacturers_obj = Manufacturer.objects.all()
    if request.method == 'POST':
        data = dict(request.POST)
        if data['manufacturers']:
            manufacturers_obj = data['manufacturers']
        if data['year_from'][0]:
            year_from = int(data['year_from'][0])
            if year_from > date.today().year or year_from < date.today().year - 25:
                year_from = date.today().year - 25
        if data['year_to'][0]:
            year_to = int(data['year_to'][0])
            if year_to > date.today().year or year_to < date.today().year - 25:
                year_to = date.today().year

        cars_obj = []
        async for car in Car.objects.all().prefetch_related('model__manufacturer'):
            if car.model.manufacturer.title in manufacturers_obj and year_to >= car.production_year >= year_from:
                cars_obj.append(car)
    manufacturers_obj = Manufacturer.objects.all()

    context = {
        'cars': cars_obj,
        'manufacturers': manufacturers_obj,
        'year_from': year_from,
        'year_to': year_to,
    }
    return await sync_to_async(render)(request, 'cars.html', context=context)


async def drivers_profile(request, pk):
    driver = await Driver.objects.aget(pk=pk)
    d_trips = [trip async for trip in Trip.objects.filter(driver=driver)]
    d_comments = Comment.objects.select_related('trip__driver')
    d_comments = [comment async for comment in d_comments if comment.trip.driver == driver]

    context = {
        'driver': driver,
        'd_trips': d_trips,
        'd_comments': d_comments,
        'd_trips_count': len(d_trips),
    }
    return await sync_to_async(render)(request, 'drivers_profile.html', context=context)


async def cars_profile(request, pk):
    car = await Car.objects.aget(pk=pk)
    c_trips = [trip async for trip in Trip.objects.filter(car=car)]
    c_comments = Comment.objects.select_related('trip__car')
    c_comments = [comment async for comment in c_comments if comment.trip.car == car]

    context = {
        'car': car,
        'c_trips': c_trips,
        'c_comments': c_comments,
        'c_trips_count': len(c_trips),
    }
    return await sync_to_async(render)(request, 'cars_profile.html', context=context)
