# Generated by Django 4.2.3 on 2023-08-06 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_rename_full_name_address_email_address_first_name_and_more'),
        ('orders', '0003_remove_order_order_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='selected_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userauths.address'),
        ),
    ]
