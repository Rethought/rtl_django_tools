#!/usr/bin/env python
from django.conf import settings
from django.core.management import call_command


def main():
    """Dynamically configure the Django settings with the
    minimum necessary to get Django running tests"""
    settings.configure(
        INSTALLED_APPS=('rtl_django_tools',
                        'django_nose',
                        'django.contrib.auth',
                        'django.contrib.contenttypes'),
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': '/tmp/rtl_django_tools.db',
                               'USER': '',
                               'PASSWORD': '',
                               'HOST': '',
                               'PORT': ''}},
        NOSE_ARGS=['--with-xunit', '-s', '-v'],
        AUTH_USER_MODEL="rtl_django_tools.User",
    )

    call_command('test', 'rtl_django_tools')

if __name__ == '__main__':
    main()
