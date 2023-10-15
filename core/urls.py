from django.urls import path
from . import views , Transfer

urlpatterns = [
    path('', views.index, name='index'),


    path('search-account', Transfer.search_account_number, name='search-account'),
    
]
