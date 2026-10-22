from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/problems/', include('problems.urls')),
    path('api/submissions/', include('submissions.urls')),
    path('api/battles/', include('battles.urls')),
]
