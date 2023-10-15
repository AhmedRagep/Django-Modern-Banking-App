
from django.shortcuts import render
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def search_account_number(request):
  account = Account.objects.all()

  quary = request.POST.get('account_number')
  if quary:
    account = Account.objects.filter(
      Q(account_number=quary)|
      Q(account_id=quary) 
      # تستخدم للتاكد من النتائج المسترجعة ليست مكرره
    ).distinct()

  return render(request, 'transfer/search_account_number.html',{'account':account,'quary':quary})