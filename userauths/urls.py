from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.RegisterView, name='sign-up'),
    path('sign-in', views.SignInView, name='sign-in'),
    path('logout', views.LogoutView, name='logout'),
]
