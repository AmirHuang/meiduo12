# Generated by Django 2.2.4 on 2020-06-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='default_image_url',
            field=models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='', verbose_name='默认图片'),
        ),
    ]
