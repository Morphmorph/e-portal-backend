from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='create/user/')),  # Redirect root URL to create/student/
    path('', include('userform.urls')),  # Include other URLs from userform app
]
