# project/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('myapp.urls')),
]

# app/urls.py
from django.urls import path
from myapp.views import NotificationView

urlpatterns = [
    path('api/send_notification/', NotificationView.as_view(), name='send_notification'),
    # Other URL patterns...
]
