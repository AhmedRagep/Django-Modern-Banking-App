from django.urls import path
from . import views , Transfer

urlpatterns = [
    path('', views.index, name='index'),


    path('search-account', Transfer.search_account_number, name='search-account'),
    path('amount-transfer/<account_number>', Transfer.amount_transfer, name='amount-transfer'),
    
]
