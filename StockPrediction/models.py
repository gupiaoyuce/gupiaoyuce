from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import models as auth_models
# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=10)

class stock_price(models.Model):
    stockname = models.CharField(max_length=6)
    date = models.DateField()
    open = models.DecimalField(decimal_places=3,max_digits=20)
    close = models.DecimalField(decimal_places=3,max_digits=20)
    high = models.DecimalField(decimal_places=3,max_digits=20)
    low = models.DecimalField(decimal_places=3,max_digits=20)
    volume = models.DecimalField(decimal_places=3,max_digits=20)
    code = models.CharField(max_length=6)
    class Meta:
        unique_together=('code','date')

class stock_pred(models.Model):
    date = models.DateField()
    code = models.CharField(max_length=6)
    stockname = models.CharField(max_length=6,null=True)
    macdh = models.DecimalField(decimal_places=15,max_digits=30,null=True)
    stoK =models.DecimalField(decimal_places=15,max_digits=30,null=True)
    stoD =models.DecimalField(decimal_places=15,max_digits=30,null=True)
    rsi =models.DecimalField(decimal_places=15,max_digits=30,null=True)
    willR =models.DecimalField(decimal_places=15,max_digits=30,null=True)
    ultosc =models.DecimalField(decimal_places=15,max_digits=30,null=True)
    mfi =models.DecimalField(decimal_places=15,max_digits=30,null=True)
    open = models.DecimalField(decimal_places=3, max_digits=20,null=True)
    close = models.DecimalField(decimal_places=3, max_digits=20,null=True)
    high = models.DecimalField(decimal_places=3, max_digits=20,null=True)
    low = models.DecimalField(decimal_places=3, max_digits=20,null=True)
    volume = models.DecimalField(decimal_places=3, max_digits=20,null=True)
    # down = models.BooleanField(null=True)
    # pred = models.BooleanField(null=True)
    down = models.NullBooleanField()
    pred = models.NullBooleanField()
    class Meta:
        unique_together=('code','date')
class user_follow(models.Model):
    username = models.CharField(max_length=20)
    # code = models.ForeignKey(stock_pred,verbose_name='code',on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    buy_price = models.DecimalField(decimal_places=3,max_digits=10)
    buy_date = models.DateField()
    sale_price = models.DecimalField(decimal_places=3,max_digits=10,null=True)
    sale_date = models.DateField(null=True)
    class Meta:
        unique_together=('code','username','buy_date')

class pred_anal(models.Model):
    code = models.CharField(max_length=6)
    stockname = models.CharField(max_length=6,null=True)
    hopeopen = models.DecimalField(decimal_places=15,max_digits=30,null=True)
    hopesale = models.DecimalField(decimal_places=15,max_digits=30,null=True)
    buydate = models.DateField()
    high = models.DecimalField(decimal_places=15,max_digits=20,null=True)
    highdate = models.DateField()
    chg = models.DecimalField(decimal_places=15,max_digits=20,null=True)
    class Meta:
        unique_together=('code','buydate')

class pred_anal_macdh(models.Model):
    code = models.CharField(max_length=6)
    stockname = models.CharField(max_length=6,null=True)
    hopeopen = models.DecimalField(decimal_places=15,max_digits=30,null=True)
    hopesale = models.DecimalField(decimal_places=15,max_digits=30,null=True)
    buydate = models.DateField()
    high = models.DecimalField(decimal_places=15,max_digits=20,null=True)
    highdate = models.DateField()
    chg = models.DecimalField(decimal_places=15,max_digits=20,null=True)
    class Meta:
        unique_together=('code','buydate')
