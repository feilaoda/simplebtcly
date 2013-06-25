from btcly.settings import *

import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'btcly',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': 'localhost'
    }
}

SECRET_KEY = 'fake-key'

LANGUAGE_CODE ='zh-cn'


