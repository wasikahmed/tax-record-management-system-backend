from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('users.urls')),
    path('api/taxes/', include('taxes.urls')),
    path('api/support/', include('support.urls')),
]