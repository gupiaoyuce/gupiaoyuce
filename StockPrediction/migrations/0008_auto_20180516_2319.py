# Generated by Django 2.0.4 on 2018-05-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockPrediction', '0007_stock_pred_stockname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_follow',
            name='code',
            field=models.CharField(max_length=6),
        ),
    ]
