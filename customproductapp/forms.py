# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:28:46 2023

@author: alann
"""
from django import forms

class IngredientForm(forms.Form):
    json_data = forms.JSONField()

