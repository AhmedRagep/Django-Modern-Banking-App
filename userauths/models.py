from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  username = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  # تعريف اسم المستخدم علي انه الايميل
  USERNAME_FIELD = 'email'
  # لجعله مطلوب
  REQUIRED_FIELDS = ['username']

  def __str__(self):
      return self.username
