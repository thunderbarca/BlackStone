import logging
from settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'postgres',
        'PASSWORD': 'sh@dow',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# 设置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose_format': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple_format': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
        'standard_format': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(pathname)s:%(lineno)d]'
                      '[func:%(funcName)s][%(levelname)s][%(message)s]'}
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_format'
        },
        'file': {
            # 实际开发建议使用WARNING
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR
            'filename': str(BASE_DIR.joinpath("data/logs/info.log")),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'standard_format'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

logger = logging.getLogger('django')
