"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k9_#b)b8st63^y3zhi$vcky*no_dn&!v)asya87*+z%f4b27lc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.meiduo.site','127.0.0.1']


# Application definition
import sys
#告诉系统apps作为了子应用的新的导包路径
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
# print(sys.path)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'verifications.apps.VerificationsConfig',
    'contents.apps.ContentsConfig',
    'oauth.apps.OauthConfig',
    'areas.apps.AreasConfig',
    'goods.apps.GoodsConfig',
    'haystack',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'django_crontab'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment':'meiduo_mall.utils.jinja2_env.environment', #指定模块加载的环境
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'meiduo12',
    #     'USER': 'root',
    #     'PASSWORD': '123456',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    # },
    'default': { #主(写)
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo12',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '172.16.12.134',
        'PORT': '3306',
    },
    'slave': { #从(读)
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo12',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '172.16.12.134',
        'PORT': '8306',
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]


#redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

#日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别,INFO < debug < warn < error
        },
    }
}
#指定用户模型类
AUTH_USER_MODEL = 'users.User'

#指定认证后端
AUTHENTICATION_BACKENDS = ['meiduo_mall.utils.authenticate.MyAuthenticateBackend']

#用户若是没有登陆,到这来
LOGIN_URL = "/login/"

#qq配置
QQ_CLIENT_ID = '101518219'
QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'

#邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
EMAIL_HOST = 'smtp.163.com' # 发邮件主机
EMAIL_PORT = 25 # 发邮件端口
EMAIL_HOST_USER = 'jinghedeveloper@163.com' # 授权的邮箱
EMAIL_HOST_PASSWORD = 'abcd1234' # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<jinghedeveloper@163.com>' # 发件人抬头
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8000/emails/verification/'

#指定storage的位置
BASE_URL = "http://image.meiduo.site:8888/"

#指定自己的文件存储类
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fdfs.MyFileStorage.MyStorage'

#haystack配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://172.16.12.134:9200/', #es默认端口
        'INDEX_NAME': 'haystack',
    },
}
#使搜索索引保持最新
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
#每页显示的结果数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5

#支付宝
APLIPAY_PRIVATE_KEY = os.path.join(BASE_DIR,'apps/payment/keys/app_private_key.pem')
APLIPAY_PUBLIC_KEY = os.path.join(BASE_DIR,'apps/payment/keys/app_public_key_ali.pem')
ALIPAY_APPID = '2016092700606753'
ALIPAY_DEBUG = False
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do?'
ALIPAY_RETURN_URL = 'http://www.meiduo.site:8000/payment/status/'

#定时任务
CRONJOBS = [
    # 第一颗星: 分
    # 第二颗星: 时
    # 第三颗星: 日
    # 第四颗星: 月
    # 第五颗星: 周
    # 每1分钟生成一次首页静态文件, 参数2,需要执行的方法,  参数3,日志文件的存放位置
    ('*/1 * * * *', 'contents.crons.generate_static_index_html', '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'logs/crontab.log'))
]
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

#获取读写的数据库
DATABASE_ROUTERS = ['meiduo_mall.utils.db_routers.MasterSlaveDBRouter']

#指定静态文件的收集位置
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')