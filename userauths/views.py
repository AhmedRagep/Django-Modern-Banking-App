from django.shortcuts import redirect, render
from .forms import UsreRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import User
# Create your views here.

def RegisterView(request):
  if request.method == 'POST':
    form = UsreRegisterForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      # جلب الاسم
      username = form.cleaned_data.get('username')
      # رسالة للمستخدم
      messages.success(request, f'Hey {username} your account was created successfully.')
      # مساواة الاسم بالايميل لانه المطلوب وايضا الباسورد
      new_user = authenticate(username=form.cleaned_data['email'],
                              password=form.cleaned_data['password1'])

      # تسجيل الدخول
      login(request, new_user)
      return redirect('index')
    
  # اذا كان اليوزر مسجل يتم اعادة توجيه الي الصفحة الرئيسيه
  if request.user.is_authenticated:
    messages.warning(request, f'You are already logged in!')
    return redirect('index')
      
  else:
    form = UsreRegisterForm()
  return render(request, 'userauths/sign-up.html',{'form':form})



def SignInView(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
      # هات الايميل اللي بيساوي الايميل اللي اتكتب
      user = User.objects.get(email=email)
      # ساوي المعلومات
      user = authenticate(request, email=email, password=password)

      # لو اليوزر مش فاضي بمعني اتكتب فيه
      if user is not None:
        # سجل دخول بيه
        login(request, user)
        messages.success(request, 'You are logged In.')
        return redirect('index')
      else:
        messages.warning(request, 'Username or Password does not exist!')
        return redirect('sign-in')
    except:
      messages.warning(request, 'User does not exist!')
  return render(request, 'userauths/sign-in.html')




def LogoutView(request):
  logout(request)
  messages.error(request, 'Logged Out!...')
  return redirect('sign-in')