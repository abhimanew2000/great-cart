# Generated by Django 4.2.3 on 2023-08-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_productgallery_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgallery',
            name='cropped_image',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
