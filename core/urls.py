from django.urls import path
from . import views , Transfer

urlpatterns = [
    path('', views.index, name='index'),


    path('search-account', Transfer.search_account_number, name='search-account'),
    path('amount-transfer/<account_number>', Transfer.amount_transfer, name='amount-transfer'),
    path('amount-transfer-process/<account_number>', Transfer.amount_transfer_Process, name='amount-transfer-process'),
    path('transfer-confirmation/<account_number>/<transaction_id>', Transfer.transfer_confirmation, name='transfer-confirmation'),
    path('transfer-process/<account_number>/<transaction_id>', Transfer.transfer_process, name='transfer-process'),
    
]
