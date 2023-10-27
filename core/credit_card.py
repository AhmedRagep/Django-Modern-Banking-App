from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account

def card_detail(request, card_id):
  account = Account.objects.get(user=request.user)
  credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

  context = {
    'account': account,
    'credit_card': credit_card
  }

  return render(request, "credit_card/card-detail.html", context)


def fund_credit_card(request, card_id):
  credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
  account = request.user.account

  if request.method == 'POST':
    # هات الرقم اللي كتبه اليوزر
    amount = request.POST.get('funding_amount') # 25

    # لو القيمه اللي جبتها اقل من او تساوي قيمة الحساب
    if Decimal(amount) <= account.account_balance:
      # اخصم القيمة من الحساب
      account.account_balance -= Decimal(amount)
      account.save()

      # ضيف القيمه في الفيزا
      credit_card.amount += Decimal(amount)
      credit_card.save()

      messages.success(request, 'Finding Successfully.')
      return redirect('card-detail', credit_card.card_id)
    else:
      messages.warning(request, 'Error Funds!')
      return redirect('card-detail', credit_card.card_id)
    


def withdraw_fund(request, card_id):
  account = Account.objects.get(user=request.user)
  credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

  if request.method == 'POST':
    amount = request.POST.get('amount')

    if credit_card.amount >= Decimal(amount):
      account.account_balance += Decimal(amount)
      account.save()

      credit_card.amount -= Decimal(amount)
      credit_card.save()

      messages.success(request, 'Withdrawal Successfull')
      return redirect('card-detail', credit_card.card_id)
    else:
      messages.warning(request, 'Error Funds')
      return redirect('card-detail', credit_card.card_id)

  

def delete_card(request, card_id):
  credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
  
  # New Feature
  # BEfore deleting card, it'll be nice to transfer all the money from the card to the main account balance.
  account = request.user.account
    
  if credit_card.amount > 0:
    account.account_balance += credit_card.amount
    account.save()
        
    credit_card.delete()
    messages.success(request, "Card Deleted Successfull")
    return redirect("dashboard")
    
  credit_card.delete()
  messages.success(request, 'Card Deleted Successfully.')
  return redirect('dashboard')