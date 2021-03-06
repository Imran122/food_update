# Generated by Django 2.2.20 on 2021-05-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210515_0533'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('order', models.CharField(max_length=40, null=True)),
                ('payment_method', models.CharField(max_length=40, null=True)),
                ('amount', models.FloatField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='payment_type',
            field=models.CharField(choices=[('P', 'PAYPAL'), ('S', 'STRIPE'), ('F', 'NO PAYMENT')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='subscription_type',
            field=models.CharField(choices=[('F', 'FREE'), ('M', 'MONTHLY'), ('Y', 'YEARLY')], default='F', max_length=100),
        ),
    ]
