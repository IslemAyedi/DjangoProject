# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 22:01:20 2023

@author: alann
"""

from pulp import *

def optimize_whiskas_problem(data):
    # Extract variables from the JSON data
    Ingredients = data["Ingredients"]
    costs = data["Costs"]
    proteinPercent = data["ProteinPercent"]
    fatPercent = data["FatPercent"]
    fibrePercent = data["FibrePercent"]
    saltPercent = data["SaltPercent"]

    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("The Whiskas Problem", LpMinimize)

    # A dictionary called 'ingredient_vars' is created to contain the referenced Variables
    ingredient_vars = LpVariable.dicts("Ingr", Ingredients, 0)

    # The objective function is added to 'prob' first
    prob += (
        lpSum([costs[i] * ingredient_vars[i] for i in Ingredients]),
        "Total Cost of Ingredients per can",
    )

    # Add constraints
    prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 100, "PercentagesSum"
    prob += (
        lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 8.0,
        "ProteinRequirement",
    )
    prob += (
        lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 6.0,
        "FatRequirement",
    )
    prob += (
        lpSum([fibrePercent[i] * ingredient_vars[i] for i in Ingredients]) <= 2.0,
        "FibreRequirement",
    )
    prob += (
        lpSum([saltPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.4,
        "SaltRequirement",
    )

    # Solve the optimization problem
    prob.solve()

    # Return the optimization results (variables and objective value)
    results = {
        "status": LpStatus[prob.status],
        "variables": {
            var.name: var.varValue for var in prob.variables() if var.varValue > 0
        },
        "objective_value": value(prob.objective),
    }

    return results
