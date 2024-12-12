from gurobipy import Model, GRB

def optimize_whiskas_problem(data):
    Ingredients = data["Ingredients"]
    costs = data["Costs"]
    proteinPercent = data["ProteinPercent"]
    fatPercent = data["FatPercent"]
    fibrePercent = data["FibrePercent"]
    saltPercent = data["SaltPercent"]

    model = Model("BlendingOptimization")

   
    ingredient_vars = {
        ingredient: model.addVar(vtype=GRB.CONTINUOUS, name=ingredient, lb=0, ub=100)
        for ingredient in Ingredients
    }

    model.setObjective(
        sum(costs[ingredient] * ingredient_vars[ingredient] for ingredient in Ingredients),
        GRB.MINIMIZE
    )

    model.addConstr(
        sum(ingredient_vars[ingredient] for ingredient in Ingredients) == 100,
        "TotalProportions"
    )

    model.addConstr(
        sum(proteinPercent[ingredient] * ingredient_vars[ingredient] for ingredient in Ingredients) >= 8.0,  
        "ProteinRequirement"
    )
    model.addConstr(
        sum(fatPercent[ingredient] * ingredient_vars[ingredient] for ingredient in Ingredients) >= 6.0, 
        "FatRequirement"
    )
    model.addConstr(
        sum(fibrePercent[ingredient] * ingredient_vars[ingredient] for ingredient in Ingredients) <= 2.0, 
        "FibreLimit"
    )
    model.addConstr(
        sum(saltPercent[ingredient] * ingredient_vars[ingredient] for ingredient in Ingredients) <= 0.4, 
        "SaltLimit"
    )

    model.setParam("MIPGap", 0.0001) 
    model.setParam("TimeLimit", 300)  

    model.optimize()

    if model.status != GRB.OPTIMAL:
        return {
            "status": "Optimization was not successful",
            "variables": {},
            "objective_value": None,
            "error": f"Model status: {model.status}, message: {model.status}",
        }

    results = {
        "status": "Optimal",
        "variables": {
            var.varName: round(var.x, 3) for var in model.getVars() if var.x > 0
        },
        "objective_value": round(model.objVal, 3),
    }

    return results
