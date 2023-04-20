from asgiref.sync import sync_to_async
from trips.models import Trip
from .models import Car, Driver
from datetime import datetime, timedelta


async def refresh_db():
    check_time = datetime.now() - timedelta(hours=10)
    async for trip in Trip.objects.filter(end__gte=check_time).select_related('driver', 'car'):
        if trip.end <= datetime.now():
            driver = Driver(
                pk=trip.driver.pk,
                free=True
            )
            await sync_to_async(driver.save)(update_fields=['free'])
            car = Car(
                pk=trip.car.pk,
                free=True
            )
            await sync_to_async(car.save)(update_fields=['free'])
