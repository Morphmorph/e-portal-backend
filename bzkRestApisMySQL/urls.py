from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='api/user/')),  # Redirect root URL to api/user/
    path('', include('userform.urls')),  # Include other URLs from userform app
]
