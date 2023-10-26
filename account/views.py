from django.shortcuts import redirect, render
from .models import KYC,Account
from .forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
# Create your views here.

# @login_required
def account(request):
  if request.user.is_authenticated:
    try:
      kyc = KYC.objects.get(user=request.user)
    except:
      messages.warning(request, 'You need to submited your KYC')
      return redirect('kyc-reg')
  else:
    messages.warning(request, 'You need to logged in!')
    return redirect('sign-in')
  
  account = Account.objects.get(user=request.user)
  return render(request, 'account/account.html',{'account':account,'kyc':kyc})


@login_required
def kyc_registration(request):
  account = Account.objects.get(user=request.user)
  user = request.user

  try:
    # لو فيه معلومات اليوزر ضافها قبل كده
    kyc = KYC.objects.get(user=user)
  except:
    # لو مفيش خليها فاضيه
    kyc = None

  if request.method == "POST":
    form = KYCForm(request.POST, request.FILES, instance=kyc)
    if form.is_valid():
      # لا تحفظ الان
      new_form = form.save(commit=False)
      # اليوزر = اليوزر
      new_form.user = user
      # الاكونت = الاكونت
      new_form.account = account
      new_form.save()
      messages.success(request, "kYC form submitted successfully, In review now.")
      return redirect('index')
  else:
    form = KYCForm(instance=kyc)

  context = {
    'form': form,
    'account':account,
    'kyc':kyc,
  }

  return render(request, 'account/kyc-form.html', context)





def dashboard(request):
  if request.user.is_authenticated:
    try:
      kyc = KYC.objects.get(user=request.user)
    except:
      messages.warning(request, 'You need to submited your KYC')
      return redirect('kyc-reg')
    
    if request.method == 'POST':
      form = CreditCardForm(request.POST)
      if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = request.user
        new_form.save()

        card_id = new_form.card_id
        messages.success(request, 'Card Added Successfully.')
        return redirect('dashboard')
    
    else:
      form = CreditCardForm()

  else:
    messages.warning(request, 'You need to logged in!')
    return redirect('sign-in')
  
  account = Account.objects.get(user=request.user)

  context = {
    'account':account,
    'kyc':kyc,
    'form':form,
  }
  return render(request, 'account/dashboard.html',context)