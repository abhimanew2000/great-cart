# Generated by Django 4.2.3 on 2023-08-17 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_razorpay_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Razorpay_Order',
        ),
    ]
