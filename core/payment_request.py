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


@login_required
def amount_request(request, account_number):
  account = Account.objects.get(account_number=account_number)

  return render(request, 'payment_request/amount-request.html', {'account':account})


@login_required
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
  


@login_required
def amount_request_confirmation(request, account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  return render(request, 'payment_request/amount-request-confirmation.html', {'account':account,'transaction':transaction})


@login_required
def amount_request_final(request, account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  if request.method == 'POST':
    pin_number = request.POST.get("pin-number")
    if pin_number == request.user.account.pin_number:
      transaction.status = "completed"
      transaction.save()
      messages.success(request, 'Your payment request have been sent successfully.')
      return redirect('amount-request-completed', account.account_number, transaction.transaction_id)
    
    else:
      messages.warning(request, 'An Error Occurd, try again later!')
      return redirect('dashboard')
    

@login_required
def amount_request_completed(request, account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  context = {
    'account':account,
    'transaction':transaction,
  }

  return render(request, 'payment_request/amount-request-completed.html', context)




# Settled

def settlement_confirmation(request, account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  context = {
    'account':account,
    'transaction':transaction,
  }

  return render(request, 'payment_request/settlement-confirmation.html', context)



def settlement_pricessing(request, account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  sender = request.user
  sender_account = request.user.account

  if request.method == "POST":
    pin_number = request.POST.get("pin-number")
    if pin_number == request.user.account.pin_number:
      if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
        messages.warning(request, "Incufficient Funds, fund your account and try againg.")
      else:
        sender_account.account_balance -= transaction.amount
        sender_account.save()

        account.account_balance += transaction.amount
        account.save()

        transaction.status = "request_settled"
        transaction.save()

        messages.success(request, f"Settled to {account.user.kyc.full_name} was successfully.")
        return redirect('settled-completed', account.account_number, transaction.transaction_id)
    
    else:
      messages.warning(request, 'Incorrect PIN')
      return redirect('settlement-confirmation', account.account_number, transaction.transaction_id)
    
  else:
    messages.warning(request, 'Error Occured')
    return redirect('dashboard')
    


def settled_completed(request,account_number, transaction_id):
  account = Account.objects.get(account_number=account_number)
  transaction = Transaction.objects.get(transaction_id=transaction_id)

  context = {
    'account':account,
    'transaction':transaction,
  }

  return render(request, 'payment_request/settled-completed.html', context)