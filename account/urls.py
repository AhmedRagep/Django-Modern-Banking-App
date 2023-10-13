from django.urls import path
from . import views

urlpatterns = [
    path('kyc-reg',views.kyc_registration, name='kyc-reg'),
]
