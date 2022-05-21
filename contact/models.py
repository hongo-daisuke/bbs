from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class ContactType(models.Model):
    class Meta(object):
        db_table = 'contact_type'
    contact_type = models.CharField(verbose_name='お問合せ種類', max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='作成日',  default=timezone.now, blank=True, null=True)
    update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
    del_flg = models.BooleanField(verbose_name='削除', default=0, blank=True, null=True)

    def __str__(self):
        return self.contact_type

class Contact(models.Model):
    class Meta(object):
        db_table = 'contact'
    user_name = models.CharField(verbose_name='お問合せ者様名', max_length=255, blank=True, null=True)
    user_mail = models.EmailField(verbose_name='お問合せ者様メールアドレス', max_length=100, blank=True, null=True)
    contact_type = models.ForeignKey(ContactType, verbose_name='板ID', null=True, on_delete=models.PROTECT)
    contact = models.TextField(verbose_name='お問合せ内容', max_length=1000, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='作成日',  default=timezone.now, blank=True, null=True)
    update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
    del_flg = models.BooleanField(verbose_name='削除', default=0, blank=True, null=True)

    def __str__(self):
        return self.contact