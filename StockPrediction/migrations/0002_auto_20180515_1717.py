# Generated by Django 2.0.4 on 2018-05-15 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StockPrediction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='stock_pred',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('code', models.CharField(max_length=6)),
                ('macdh', models.DecimalField(decimal_places=6, max_digits=15)),
                ('stoK', models.DecimalField(decimal_places=6, max_digits=15)),
                ('stoD', models.DecimalField(decimal_places=6, max_digits=15)),
                ('rsi', models.DecimalField(decimal_places=6, max_digits=15)),
                ('willR', models.DecimalField(decimal_places=6, max_digits=15)),
                ('ultosc', models.DecimalField(decimal_places=6, max_digits=15)),
                ('mfi', models.DecimalField(decimal_places=6, max_digits=15)),
                ('down', models.BooleanField()),
                ('pred', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='user_follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('buy_price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('buy_date', models.DateField()),
                ('sale_price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('sale_date', models.DateField(null=True)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StockPrediction.stock_pred', verbose_name='code')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='stock_pred',
            unique_together={('code', 'date')},
        ),
    ]