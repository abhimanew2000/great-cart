# Generated by Django 4.2.3 on 2023-07-17 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_emailverification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailVerification',
        ),
    ]
