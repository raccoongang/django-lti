from django.conf import settings


LTI_DEBUG = getattr(settings, 'LTI_DEBUG', True)
CONSUMER_KEY = getattr(settings, 'CONSUMER_KEY', "__consumer_key__")
LTI_SECRET = getattr(settings, 'LTI_SECRET', "__lti_secret__")
