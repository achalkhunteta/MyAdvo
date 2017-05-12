"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='create_form/')),
    url(r'^create_form/$', CreateForm.as_view(), name='create_form'),
    url(r'^save_form/$', SaveForm.as_view(), name='save_form'),
    url(r'^view_form/(?P<pk>\d+)', ViewForm.as_view(), name='view_form'),
    url(r'^delete_form/(?P<pk>\d+)', DeleteForm.as_view(), name='delete_form'),
    url(r'^list_forms/$', ListForm.as_view(), name='list_form')
]