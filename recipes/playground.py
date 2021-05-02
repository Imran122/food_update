import requests
import json

apiKey = '04162bc40c7b427daaa43e35cb3fd42c'

"""Get recipe from provided URL"""
        
recipeUrl = "https://www.allrecipes.com/recipe/265805/zucchini-ribbon-and-spinach-saute/"

url = f'https://api.spoonacular.com/recipes/extract?apiKey={apiKey}'
recipeUrl = recipeUrl
querystring = {"url":recipeUrl, "includeNutrition":'true'}
r = requests.request("GET", url, params=querystring)

data = r.json()

nutrients = data['nutrition']['nutrients']
nutrition = []

for nutrient in nutrients:
    if nutrient['title'] == 'Calories':
        calories = nutrient['amount']
        caloriesUnit = nutrient['unit']
        needsCalories = nutrient['percentOfDailyNeeds']
        caloriesArray = {
            'calories':{
                'amount': calories,
                'unit': caloriesUnit,
                'percent': needsCalories
            }
        }
        nutrition.append(caloriesArray)
    elif nutrient['title'] == 'Fat':
        fat = nutrient['amount']
        fatUnit = nutrient['unit']
        needsFat = nutrient['percentOfDailyNeeds']
        fatArray = {
            'fat':{
                'amount': fat,
                'unit': fatUnit,
                'percent': needsFat
            }
        }
        nutrition.append(fatArray)
    elif nutrient['title'] == 'Carbohydrates':
        carbohydrate = nutrient['amount']
        carbUnit = nutrient['unit']
        needsCarb = nutrient['percentOfDailyNeeds']
        carbsArray = {
            'carbohydrates':{
                'amount': carbohydrate,
                'unit': carbUnit,
                'percent': needsCarb
            }
        }
        nutrition.append(carbsArray)
    elif nutrient['title'] == 'Protein':
        protein = nutrient['amount']
        proteinUnit = nutrient['unit']
        needsProtein = nutrient['percentOfDailyNeeds']
        proteinArray = {
            'protein':{
                'amount': protein,
                'unit': proteinUnit,
                'percent': needsProtein
            }
        }
        nutrition.append(proteinArray)
    
    
print(nutrition[1]['fat']) 