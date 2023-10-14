from django.shortcuts import redirect, render
from .models import KYC,Account
from .forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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