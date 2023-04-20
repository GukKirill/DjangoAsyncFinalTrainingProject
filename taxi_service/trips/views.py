import time
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync, sync_to_async
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from taxi_depot.models import Driver, Car
from trips.models import Trip
from django.contrib import messages
from taxi_depot.services import refresh_db


@sync_to_async
@login_required
@async_to_sync
async def choose_driver(request, pk):
    await refresh_db()
    drivers = None
    async for car in Car.objects.filter(pk=pk).prefetch_related('drivers'):
        drivers = car.drivers.all()

    context = {
        'drivers': drivers,
        'car_pk': pk,
    }
    return await sync_to_async(render)(request, 'trips/choose_driver.html', context=context)


@sync_to_async
@login_required
@async_to_sync
async def choose_car(request, pk):
    await refresh_db()
    cars = None
    async for driver in Driver.objects.filter(pk=pk).prefetch_related('cars'):
        cars = driver.cars.all()

    context = {
        'cars': cars,
        'driver_pk': pk,
    }
    return await sync_to_async(render)(request, 'trips/choose_car.html', context=context)


@sync_to_async
@login_required
@async_to_sync
async def choose_route(request, driver_pk, car_pk):
    driver = await Driver.objects.aget(pk=driver_pk)
    car = await Car.objects.aget(pk=car_pk)
    points = ['Old Kent Road', 'Whitechapel Road', "King's Cross Station", 'The Angel, Islington', 'Euston Road',
              'Pentonville Road', 'Pall Mall', 'Electric Company', 'Whitehall', 'Northumberland Avenue',
              'Marylebone Station', 'Bow Street', 'Marlborough Street', 'Vine Street', 'The Strand', 'Fleet Street',
              'Trafalgar Square', 'Fenchurch St Station', 'Leicester Square', 'Coventry Street', 'Water Works',
              'Piccadilly', 'Regent Street', 'Oxford Street', 'Bond Street', 'Liverpool Street Station',
              'Park Lane', 'Mayfair']
    is_calculated = False
    start_point = None
    end_point = None
    cost = 1
    if request.method == 'POST':
        data = dict(request.POST)
        if data['start_point']:
            start_point = data['start_point'][0]
        else:
            end_point = None
            await sync_to_async(messages.success)(request, 'Select trip points')
        if data['end_point']:
            end_point = data['end_point'][0]
        else:
            start_point = None
            await sync_to_async(messages.success)(request, 'Select trip points')
        if start_point and end_point and start_point != end_point:
            is_calculated = True
        else:
            await sync_to_async(messages.success)(request, 'Select two different points')

    context = {
        'driver': driver,
        'car': car,
        'points': points,
        'is_calculated': is_calculated,
        'start_point': start_point,
        'end_point': end_point,
        'cost': cost,
    }
    return await sync_to_async(render)(request, 'trips/choose_route.html', context=context)


@sync_to_async
@login_required
@async_to_sync
async def trip_confirmation(request, driver_pk, car_pk, start, end, cost):
    driver = await Driver.objects.aget(pk=driver_pk)
    car = await Car.objects.aget(pk=car_pk)
    if request.method == 'POST':
        data = dict(request.POST)
        driver = await Driver.objects.aget(pk=int(data['driver'][0]))
        car = await Car.objects.aget(pk=int(data['car'][0]))
        if driver.free is True and car.free is True:
            new_trip = Trip(
                end=datetime.now()+timedelta(minutes=1),
                car=car,
                driver=driver,
                client=request.user,
                start_point=data['start_point'][0],
                end_point=data['end_point'][0],
                cost=int(data['cost'][0])
            )
            await sync_to_async(new_trip.save)()
            driver = Driver(
                pk=int(data['driver'][0]),
                free=False
            )
            await sync_to_async(driver.save)(update_fields=['free'])
            car = Car(
                pk=int(data['car'][0]),
                free=False
            )
            await sync_to_async(car.save)(update_fields=['free'])
            await sync_to_async(messages.success)(request, 'New trip is created')
        else:
            await sync_to_async(messages.success)(request, 'Driver or car are busy. Choose other ')
        return await sync_to_async(redirect)('home')

    context = {
        'driver': driver,
        'car': car,
        'start_point': start,
        'end_point': end,
        'cost': cost,
    }
    return await sync_to_async(render)(request, 'trips/trip_confirmation.html', context=context)
