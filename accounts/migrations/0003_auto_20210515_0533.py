# Generated by Django 2.2.20 on 2021-05-15 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210423_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='customer_email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='customer_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='payment_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='payment_type',
            field=models.CharField(choices=[('P', 'PAYPAL'), ('S', 'STRIPE')], max_length=20, null=True),
        ),
    ]
