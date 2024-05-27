from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('api/', include('userform.urls')),  # Include other URLs from userform app
]
