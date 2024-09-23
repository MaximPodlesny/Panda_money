from django.db import models

# Create your models here.
# class PhoneVerification(models.Model):
#     phone = models.CharField(max_length=15)
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.phone
    

# class Client(models.Model):
#     phone = models.CharField(max_length=15, unique=True)
#     first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
#     last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
#     middle_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество")
#     email = models.EmailField(null=True, blank=True, verbose_name="Электронная почта")
#     inn = models.CharField(max_length=12, null=True, blank=True, verbose_name="ИНН")
#     identity_document = models.CharField(max_length=20, null=True, blank=True, verbose_name="Удостоверение личности")
#     code = models.CharField(max_length=6)
#     phone_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")
class Client(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество")
    email = models.EmailField(null=True, blank=True, verbose_name="Электронная почта")
    inn = models.CharField(max_length=12, null=True, blank=True, verbose_name="ИНН")
    identity_document = models.CharField(max_length=20, null=True, blank=True, verbose_name="Удостоверение личности")
    code = models.CharField(max_length=6)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")

    # Новые поля
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Сумма")
    term = models.IntegerField(null=True, blank=True, verbose_name="Срок")
    currency = models.CharField(max_length=10, null=True, blank=True, verbose_name="Валюта")
    time_unit = models.CharField(max_length=10, null=True, blank=True, verbose_name="Единица времени")

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = "Заявка на займ"
        verbose_name_plural = "Заявки на займ"
        ordering = ['-created_at']