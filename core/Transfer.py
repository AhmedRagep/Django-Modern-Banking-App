
from django.shortcuts import redirect, render
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Transaction

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


@login_required
def amount_transfer(request, account_number):
  try:
    account = Account.objects.get(account_number=account_number)
  except:
    messages.warning(request, 'Account does not exist!')
    return redirect('search-account')

  return render(request, 'transfer/amount_transfer.html',{'account':account})


@login_required
# تحويل المبالغ
def amount_transfer_Process(request,account_number ):
  # جلب الاكونت صاحب الايدي الذي تم الضغط عليه
  account = Account.objects.get(account_number=account_number)
  # الشخص اللذي سيرسل الاموال هوا اليوزر
  sender = request.user
  # الشخص اللذي سوف يستلم الاموال هو اليوزر صاحب الاكونت السابق
  reciever = account.user

  # جلب اكونت اليوزر الحالي
  sender_account = request.user.account
  # جلب اكونت المستلم
  reciever_account = account

  if request.method == 'POST':
    # هات دول من صفحة العرض
    amount = request.POST.get("amount-send")
    description = request.POST.get("description")

    # لو رصيد اليوزر الحالي اكبر من 0 او هوا كتب رصيد في العرض
    if sender_account.account_balance > 0 and amount:
      # اعمل معاملة جديد بالمعلومات السابقه
      new_transaction = Transaction.objects.create(
        user = request.user,
        amount=amount,
        description = description,
        reciever = reciever,
        sender=sender,
        sender_account=sender_account,
        reciever_account = reciever_account,
        status = "processing",
        transaction_type = "transfer",
      )
      # احفظ المعاملة
      new_transaction.save()
      
      # هات رقم المعامله الذي انشئناه
      transaction_id = new_transaction.transaction_id
      # التوجه الي هذه الصفحة مع ارسال رقم الحساب اللذي ارسلنا الاموال اليه ورقم العملية
      return redirect("transfer-confirmation", account.account_number, transaction_id)
    else:
      messages.warning(request, "Insufficient Found.")
      return redirect("amount-transfer", account.account_number)
  else:
    messages.warning(request, "Error Occured, Try again later.")
    return redirect("account")