from django.urls import path
from . import views

urlpatterns = [
    path('',views.account, name='account'),
    path('kyc-reg',views.kyc_registration, name='kyc-reg'),
]
