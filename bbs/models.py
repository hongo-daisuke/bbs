from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Board(models.Model):
    class Meta(object):
        db_table = 'board'
    name = models.CharField(verbose_name='板名', max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='作成日',  default=timezone.now, blank=True, null=True)
    update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
    del_flg = models.BooleanField(verbose_name='削除', default=0, blank=True, null=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    class Meta(object):
        db_table = 'thread'

    name = models.CharField(verbose_name='スレッド名', max_length=255, blank=True, null=True)
    board = models.ForeignKey(Board, verbose_name='板ID', null=True, on_delete=models.PROTECT)
    create_date = models.DateTimeField(verbose_name='作成日',  default=timezone.now, blank=True, null=True)
    update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
    del_flg = models.BooleanField(verbose_name='削除', default=0, blank=True, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    class Meta(object):
        db_table = 'comment'

    threads = models.ForeignKey(Thread, verbose_name='スレッドID', on_delete=models.PROTECT, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True, verbose_name='メンバーID',)
    user_name = models.CharField(verbose_name='書き込み者名', blank=False, null=True, max_length=100, default='名無しのユーザー')
    email = models.EmailField(verbose_name='書き込み者メールアドレス', max_length=100, blank=True, null=True)
    ip_addr = models.GenericIPAddressField(verbose_name='書き込み者ipアドレス', max_length=100, blank=True, null=True)
    comment = models.TextField(verbose_name='コメント', max_length=1000, blank=True, null=True)
    comment_image = models.ImageField(upload_to='images', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='作成日',  default=timezone.now, blank=True, null=True)
    update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
    del_flg = models.BooleanField(verbose_name='削除', default=0, blank=True, null=True)
    
    def __str__(self):
        return self.comment