# django-lti
LTI django application designed to work with socraticqs2

Installation
------------
::

    python setup.py sdist && pip install dist/django-lti-0.1.tar.gz --upgrade
    pip install -r requirments.txt


Configuration
-------------

Add 'lti' app and some params to your settings.py:
::

    INSTALLED_APPS = (
        ....
        'lti',
        ....
    )

    # LTI Parameters
    CONSUMER_KEY = "__consumer_key__"
    LTI_SECRET = "__lti_secret__"
    X_FRAME_OPTIONS = "ALLOW-FROM: *"
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


Include 'lti.urls' to project urls.py:
::

    urlpatterns = patterns('',
        ....
        url(r'^lti/', include('lti.urls')),
        ....
    )
