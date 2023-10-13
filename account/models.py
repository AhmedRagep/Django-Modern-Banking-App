from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.db.models.signals import post_save
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
      


# لجلب هوية العملاء
class KYC(models.Model):
  id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  account = models.OneToOneField(Account, on_delete=models.CASCADE,blank=True, null=True)
  full_name = models.CharField(max_length=1000)
  image = models.ImageField(upload_to='kyc',default='default.jpg')
  marrital_status = models.CharField(choices=MARITAL_STATUS,max_length=40)
  gender = models.CharField(choices=GENDER,max_length=40)
  identity_type = models.CharField(choices=IDENTITY_TYPE,max_length=140)
  identity_image = models.ImageField(upload_to='kys', null=True,blank=True)
  date_of_birth = models.DateTimeField(auto_now_add=False)
  signature = models.ImageField(upload_to='kyc')

  # Address 
  country = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  city = models.CharField(max_length=100)

  # Contact Detail
  mobile = models.CharField(max_length=1000)
  fax = models.CharField(max_length=1000)
  date = models.DateTimeField(auto_now_add=True)


  def __str__(self):
      return f"{self.user}"


    

# تعريف الدالة الأولى التي ستنفذ عند إنشاء User جديد
def create_account(sender, instance, created, **kwargs):
  # تحقق إذا كان المستخدم منشأ حديثا    
  if created:
    # بنفس اسم اليوزر Account إنشاء كائن  
    Account.objects.create(user=instance)

# تعريف الدالة الثانية التي ستنفذ عند حفظ User  
def save_account(sender, instance, **kwargs):
  # حفظ كائن Account المرتبط بالمستخدم
  instance.account.save()

# ربط الدالة الأولى بإشارة post_save لـ User
post_save.connect(create_account,sender=User)
# ربط الدالة الثانية بإشارة post_save لـ User  
post_save.connect(save_account,sender=User)





