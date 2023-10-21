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