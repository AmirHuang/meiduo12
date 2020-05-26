# _*_ coding: utf-8 _*_
# @time     : 2020/05/26
# @Author   : Amir
# @Site     : 
# @File     : jinja2_env.py
# @Software : PyCharm

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
