from django.urls import path
from . import views , Transfer
from .transaction import transaction_lists,transaction_detail
from . import payment_request

urlpatterns = [
    path('', views.index, name='index'),


    path('search-account', Transfer.search_account_number, name='search-account'),
    path('amount-transfer/<account_number>', Transfer.amount_transfer, name='amount-transfer'),
    path('amount-transfer-process/<account_number>', Transfer.amount_transfer_Process, name='amount-transfer-process'),
    path('transfer-confirmation/<account_number>/<transaction_id>', Transfer.transfer_confirmation, name='transfer-confirmation'),
    path('transfer-process/<account_number>/<transaction_id>', Transfer.transfer_process, name='transfer-process'),
    path('transfer-completed/<account_number>/<transaction_id>', Transfer.transfer_completed, name='transfer-completed'),
    

    # transaction

    path('transactions', transaction_lists, name='transactions'),
    path('transactions/<transaction_id>', transaction_detail, name='transaction-detail'),

    # Payment Request
    path('request-search-account',payment_request.search_user_request, name='request-search-account'),
    path('amount-request/<account_number>',payment_request.amount_request, name='amount-request'),
    path('amount-request-process/<account_number>',payment_request.amount_request_process, name='amount-request-process'),
    path('amount-request-confirmation/<account_number>/<transaction_id>',payment_request.amount_request_confirmation, name='amount-request-confirmation'),
    path('amount-request-final/<account_number>/<transaction_id>',payment_request.amount_request_final, name='amount-request-final'),
    path('amount-request-completed/<account_number>/<transaction_id>',payment_request.amount_request_completed, name='amount-request-completed'),

    # Requst Settelment
    path('settlement-confirmation/<account_number>/<transaction_id>',payment_request.settlement_confirmation, name='settlement-confirmation'),
    path('settlement-processing/<account_number>/<transaction_id>',payment_request.settlement_pricessing, name='settlement-processing'),
    path('settled-completed/<account_number>/<transaction_id>',payment_request.settled_completed, name='settled-completed'),
]
