# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_product_view, name='custom_product_view'),
]
