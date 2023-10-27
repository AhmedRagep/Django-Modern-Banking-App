from django.urls import path
from . import views , Transfer, credit_card
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
    path('delete-payment/<account_number>/<transaction_id>',payment_request.delete_payment_request, name='delete-payment'),

    # Credit Card
    path("card/<card_id>", credit_card.card_detail, name="card-detail"),
    path("fund_credit_card/<card_id>", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>", credit_card.withdraw_fund, name="withdraw-fund"),
    path("delete_card/<card_id>", credit_card.delete_card, name="delete-card"),
]
