from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('depot/', include('taxi_depot.urls')),
    path('trips/', include('trips.urls')),
    path('users/', include('users.urls')),
    path('comment/<int:pk>/', include('comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
