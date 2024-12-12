# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:28:46 2023

@author: alann
"""
from django import forms

class CustomProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredients'] = forms.CharField(
            widget=forms.HiddenInput(), required=False
        )