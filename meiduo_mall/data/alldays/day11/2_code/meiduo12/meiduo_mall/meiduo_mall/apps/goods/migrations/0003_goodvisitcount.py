# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-02 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190602_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodVisitCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('date', models.DateField(auto_now_add=True, verbose_name='访问的日期')),
                ('count', models.IntegerField(default=0, verbose_name='数量')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_counts', to='goods.GoodsCategory', verbose_name='分类')),
            ],
            options={
                'db_table': 'tb_goods_visit',
            },
        ),
    ]