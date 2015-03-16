from django.conf.urls import url, patterns, include
from django.utils import importlib


urlpatterns = patterns('',
    url(r'^/*$', 'lti.views.index', name='lti_index'),
)
