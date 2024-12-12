from django.urls import path
from . import views

urlpatterns = [
    path('optimize/', views.optimize_view, name='optimize'),
    path('food/', views.custom_product_view, name='custom_product_view'),
    path('intermediate/', views.intermediate_page, name='intermediate'),
    path('chimical/', views.chimical_page, name='chimical'),
    path('chemical-form/', views.chemical_optimization_view, name='chemical_form'),
    path('chemical-results/', views.chemical_optimization_view, name='chemical_results'),
    path("", views.main, name="main"),
]
