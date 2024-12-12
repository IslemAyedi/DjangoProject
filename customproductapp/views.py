from django import forms
from django.shortcuts import render
from django.http import JsonResponse
from .optimization import optimize_whiskas_problem
from django.conf import settings
from django.http import HttpResponse

from gurobipy import Model, GRB
import logging

def main(request):
    return render(request, 'main.html')

def intermediate_page(request):
    return render(request, 'intermediate.html')

def chimical_page(request):
    return render(request, 'custom_chimical_form.html')

def optimize_view(request):
    return render(request, 'summary.html')


class CustomProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        ingredients = kwargs.pop('ingredients', []) 
        super().__init__(*args, **kwargs)

        for ingredient in ingredients:
            self.fields[f'{ingredient}_cost'] = forms.FloatField(
                label=f'Cost of {ingredient} ($)',
                required=True
            )
            self.fields[f'{ingredient}_protein'] = forms.FloatField(
                label=f'Protein % in {ingredient}',
                required=True
            )
            self.fields[f'{ingredient}_fat'] = forms.FloatField(
                label=f'Fat % in {ingredient}',
                required=True
            )
            self.fields[f'{ingredient}_fibre'] = forms.FloatField(
                label=f'Fibre % in {ingredient}',
                required=True
            )
            self.fields[f'{ingredient}_salt'] = forms.FloatField(
                label=f'Salt % in {ingredient}',
                required=True
            )

def custom_product_view(request):
    if request.method == 'POST':
        # Parse dynamic ingredient data
        ingredients = request.POST.getlist('ingredients[]')
        costs = request.POST.getlist('costs[]')
        proteins = request.POST.getlist('proteins[]')
        fats = request.POST.getlist('fats[]')
        fibres = request.POST.getlist('fibres[]')
        salts = request.POST.getlist('salts[]')

        # Prepare the data dictionary
        data = {
            "Ingredients": ingredients,
            "Costs": {ingredients[i]: float(costs[i]) for i in range(len(ingredients))},
            "ProteinPercent": {ingredients[i]: float(proteins[i]) for i in range(len(ingredients))},
            "FatPercent": {ingredients[i]: float(fats[i]) for i in range(len(ingredients))},
            "FibrePercent": {ingredients[i]: float(fibres[i]) for i in range(len(ingredients))},
            "SaltPercent": {ingredients[i]: float(salts[i]) for i in range(len(ingredients))},
        }

        # Call the optimization function
        results = optimize_whiskas_problem(data)

        # Render the results page with proper context
        context = {
            "summary": {
                "TotalProtein": 8,
                "TotalFat": 6,
                "TotalFibre": 2,
                "TotalSalt": 0.4,
                "TotalCost": results["objective_value"],
            },
            "results": results,
        }
        return render(request, 'summary.html', context)

    form = CustomProductForm()
    return render(request, 'custom_product_form.html', {'form': form})

logger = logging.getLogger(__name__)

def custom_product_view(request):
    if request.method == 'POST':
        try:
            # Parse dynamic ingredient data
            ingredients = request.POST.getlist('ingredients[]')
            costs = request.POST.getlist('costs[]')
            proteins = request.POST.getlist('proteins[]')
            fats = request.POST.getlist('fats[]')
            fibres = request.POST.getlist('fibres[]')
            salts = request.POST.getlist('salts[]')

            if not ingredients or not costs or not proteins or not fats or not fibres or not salts:
                raise ValueError("All fields are required.")

            # Prepare the data dictionary
            data = {
                "Ingredients": ingredients,
                "Costs": {ingredients[i]: float(costs[i]) for i in range(len(ingredients))},
                "ProteinPercent": {ingredients[i]: float(proteins[i]) for i in range(len(ingredients))},
                "FatPercent": {ingredients[i]: float(fats[i]) for i in range(len(ingredients))},
                "FibrePercent": {ingredients[i]: float(fibres[i]) for i in range(len(ingredients))},
                "SaltPercent": {ingredients[i]: float(salts[i]) for i in range(len(ingredients))},
            }

            # Call the optimization function
            results = optimize_whiskas_problem(data)

            # Render the results page with proper context
            context = {
                "summary": {
                    "TotalProtein": 8,  # Replace with actual computation if needed
                    "TotalFat": 6,  # Replace with actual computation if needed
                    "TotalFibre": 2,  # Replace with actual computation if needed
                    "TotalSalt": 0.4,  # Replace with actual computation if needed
                    "TotalCost": results.get("objective_value", 0),
                },
                "results": results,
            }
            return render(request, 'summary.html', context)

        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            return render(request, 'custom_product_form.html', {'error': str(ve)})

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return render(request, 'custom_product_form.html', {'error': 'An unexpected error occurred. Please try again.'})

    form = CustomProductForm()
    return render(request, 'custom_product_form.html', {'form': form})


class ChemicalProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        chemicals = kwargs.pop('chemicals', [])
        super().__init__(*args, **kwargs)

        for chemical in chemicals:
            self.fields[f'{chemical}_cost'] = forms.FloatField(
                label=f'Cost of {chemical} ($)',
                required=True
            )
            self.fields[f'{chemical}_composition'] = forms.FloatField(
                label=f'Composition % in {chemical}',
                required=True
            )

def chemical_optimization_view(request):
    if request.method == 'POST':
        try:
            chemicals = request.POST.getlist('chemicals[]')
            costs = request.POST.getlist('costs[]')
            compositions = request.POST.getlist('compositions[]')

            if not chemicals or not costs or not compositions:
                raise ValueError("All fields are required.")

            # Prepare the data dictionary
            data = {
                "Ingredients": chemicals,
                "Costs": {chemicals[i]: float(costs[i]) for i in range(len(chemicals))},
                "CompositionPercent": {chemicals[i]: float(compositions[i]) for i in range(len(chemicals))},
            }

            # Call the optimization function
            results = optimize_whiskas_problem(data)

            # Render the results page with proper context
            context = {
                "results": results,
                "chemicals": data,
            }
            return render(request, 'chemical_results.html', context)

        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            return render(request, 'chemical_form.html', {'error': str(ve)})

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return render(request, 'chemical_form.html', {'error': 'An unexpected error occurred. Please try again.'})

    form = ChemicalProductForm()
    return render(request, 'chemical_form.html', {'form': form})