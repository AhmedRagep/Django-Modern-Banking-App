from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
# Create your models here.


ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)


def user_directory_path(instance, filename):
  # استخراج امتداد الملف من اسم الملف (مثل: jpg أو png)
  ext = filename.split('.')[-1]
  # إعادة تسمية الملف بحيث يحتوي على معرف النموذج وامتداد الملف
  filename = "%s_%s" % (instance.id, ext)
  # إعادة المسار النهائي الذي سيتم حفظ الملف فيه، وهو مسار مستند إلى معرف المستخدم
  # واسم الملف المعدل
  return "user_{0}/{1}".format(instance.user.id, filename)


class Account(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
  account_number = ShortUUIDField(unique=True,length=10, max_length=25, prefix="217", alphabet="1234567890")
  #                                       الرقم مكون من هذه      بداية الرقم    الحد الاقصي الحد     الادني 
  account_id = ShortUUIDField(unique=True,length=7, max_length=25, prefix="DEX", alphabet="1234567890")
  pin_number = ShortUUIDField(unique=True,length=4, max_length=7, alphabet="1234567890")
  red_code = ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefgh1234567890")
  account_status = models.CharField(max_length=50, choices=ACCOUNT_STATUS,default='in-active')
  date = models.DateTimeField(auto_now_add=True)
  kys_submitted = models.BooleanField(default=False)
  kys_confirmed = models.BooleanField(default=False)
  # - on_delete=models.DO_NOTHING: هذا يعني أنه عندما يتم حذف مستخدم مشير إليه في هذا الحقل، لن يتم اتخاذ أي إجراء تلقائيًا.
  recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True, null=True,related_name='recommended_by')


  class Meta:
    # ترتيب البيانات بناءا علي التاريخ بالعد التنازلي
    ordering = ['-date']

  def __str__(self):
      try:
        return f"{self.user}"
      except:
        return 'Account Model'