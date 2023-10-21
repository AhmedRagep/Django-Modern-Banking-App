from django.shortcuts import redirect, render
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Transaction
from decimal import Decimal



@login_required
def search_user_request(request):
  # هات كل الحسابات
  account = Account.objects.all()
  # هات رقم الحساب اللي كتبه المستخدم
  query = request.POST.get("account_number")

  # لو فيه رقم
  if query:
    # فلتر في الحسابات برقم الحساب
    account = account.filter(
      Q(account_number=query)|
      Q(account_id=query)
    ).distinct()

  context = {
    'account':account,
    'query':query,
  }

  return render(request, 'payment_request/search-users.html', context)



def amount_request(request, account_number):
  account = Account.objects.get(account_number=account_number)

  return render(request, 'payment_request/amount-request.html', {'account':account})



def amount_request_process(request,account_number):
  account = Account.objects.get(account_number=account_number)

  sender = request.user
  reciever = account.user

  sender_account = request.user.account
  reciever_account = account

  if request.method == 'POST':
    amount = request.POST.get("amount-request")
    description = request.POST.get("description")

    new_request = Transaction.objects.create(
      user = request.user,
      amount=amount,
      description=description,

      sender = sender,
      reciever = reciever,
      
      reciever_account = reciever_account,
      sender_account = sender_account,

      status = 'requests',
      transaction_type= 'request'
    )

    new_request.save()
    transaction_id = new_request.transaction_id
    return redirect('amount-request-confirmation', account.account_number, transaction_id)
  
  else:
    messages.warning(request, 'Error occured try again later.')
    return redirect('dashboard')
  



def amount_request_confirmation(request, account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  return render(request, 'payment_request/amount-request-confirmation.html', {'account':account,'transaction':transaction})