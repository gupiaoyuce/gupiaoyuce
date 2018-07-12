# Generated by Django 2.0.4 on 2018-05-15 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stock_price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockname', models.CharField(max_length=6)),
                ('date', models.DateField()),
                ('open', models.DecimalField(decimal_places=3, max_digits=12)),
                ('close', models.DecimalField(decimal_places=3, max_digits=12)),
                ('high', models.DecimalField(decimal_places=3, max_digits=12)),
                ('low', models.DecimalField(decimal_places=3, max_digits=12)),
                ('volume', models.DecimalField(decimal_places=3, max_digits=12)),
                ('code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='stock_price',
            unique_together={('code', 'date')},
        ),
    ]
