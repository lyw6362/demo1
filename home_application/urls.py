# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = (
    # url(r'^$', views.home),
    # url(r'^dev-guide/$', views.dev_guide),
    # url(r'^contact/$', views.contact),
    url(r"^$",views.index),
    url(r"result",views.result),
    url(r"login",views.login_verify),
    url(r"server_verify",views.server_verify),
    url(r"get_cpu",views.get_cpu),
)
