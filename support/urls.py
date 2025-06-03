from django.urls import path
from .views import SubmitContactUsView


urlpatterns = [
    path('contact-us/', SubmitContactUsView.as_view(), name='contact-us'),
]
