from django.shortcuts import render
from .forms import IngredientForm
# from .models import Ingredient
from .optimization import optimize_whiskas_problem


# Implement the logic to calculate the summary based on the JSON data
# You can use the provided data structures and calculate the cost, 
# protein, fat, etc.
# Return a dictionary with the summary
def calculate_summary(data):
    # Initialize summary variables
    total_cost = 0
    total_protein = 0
    total_fat = 0
    total_fibre = 0
    total_salt = 0

    # Iterate through ingredients
    for ingredient in data["Ingredients"]:
        # Get the cost, protein percent, fat percent, fibre percent, and salt percent for the ingredient
        cost = data["Costs"].get(ingredient, 0)
        protein_percent = data["ProteinPercent"].get(ingredient, 0)
        fat_percent = data["FatPercent"].get(ingredient, 0)
        fibre_percent = data["FibrePercent"].get(ingredient, 0)
        salt_percent = data["SaltPercent"].get(ingredient, 0)

        # Calculate the contribution of this ingredient to the totals
        total_cost += cost
        total_protein += cost * protein_percent
        total_fat += cost * fat_percent
        total_fibre += cost * fibre_percent
        total_salt += cost * salt_percent

    # Create a summary dictionary
    summary = {
        "TotalCost": round(total_cost, 2),
        "TotalProtein": round(total_protein, 4),
        "TotalFat": round(total_fat, 4),
        "TotalFibre": round(total_fibre, 4),
        "TotalSalt": round(total_salt, 4)
    }

    return summary


def custom_product_view(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            json_data = form.cleaned_data['json_data']
            summary = calculate_summary(json_data)
            optimization_results = optimize_whiskas_problem(json_data)
            
            return render(request, 'summary.html', 
                          {'summary': summary, 'results': optimization_results})

    else:
        form = IngredientForm()

    return render(request, 'custom_product_form.html', {'form': form})
