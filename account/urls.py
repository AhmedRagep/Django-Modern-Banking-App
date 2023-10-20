from django.urls import path
from . import views

urlpatterns = [
    path('dashboard',views.dashboard, name='dashboard'),
    path('',views.account, name='account'),
    path('kyc-reg',views.kyc_registration, name='kyc-reg'),
]
